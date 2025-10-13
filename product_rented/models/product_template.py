from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented_bolean = fields.Boolean(string="Puede ser rentado")
    rented_price = fields.Float(string="Precio de renta", oldname="rented_prince")
    rented_time_option_ids = fields.Many2many(
        comodel_name="product.rented.time.option",
        relation="product_template_rented_time_option_rel",
        column1="product_tmpl_id",
        column2="option_id",
        string="Tiempos de renta permitidos",
        help="Duraciones disponibles para rentar este producto.",
    )
    rented_description = fields.Text(string="Descripción de renta")
    rented_profit = fields.Float(string="Ganancia de renta")
