from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented_bolean = fields.Boolean(string="Puede ser rentado")
    rented_price = fields.Float(
        string="Precio de renta desde",
        oldname="rented_prince",
        compute="_compute_rented_price",
        store=True,
        help="Precio mínimo calculado automáticamente a partir de las tarifas de renta configuradas.",
    )
    rented_time_option_ids = fields.Many2many(
        comodel_name="product.rented.time.option",
        relation="product_template_rented_time_option_rel",
        column1="product_tmpl_id",
        column2="option_id",
        string="Tiempos de renta permitidos",
        help="Duraciones disponibles para rentar este producto.",
    )
    rented_time_price_ids = fields.One2many(
        comodel_name="product.rented.time.price",
        inverse_name="product_tmpl_id",
        string="Precios de renta",
        copy=True,
    )
    rented_description = fields.Text(string="Descripción de renta")
    rented_profit = fields.Float(string="Ganancia de renta")

    @api.depends("rented_time_price_ids.final_price")
    def _compute_rented_price(self):
        for product in self:
            prices = product.rented_time_price_ids.mapped("final_price")
            prices = [price for price in prices if price is not None and price is not False]
            product.rented_price = min(prices) if prices else 0.0
