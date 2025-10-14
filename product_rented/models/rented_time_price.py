from odoo import api, fields, models


class ProductRentedTimePrice(models.Model):
    _name = "product.rented.time.price"
    _description = "Precio por opción de tiempo de renta"
    _order = "product_tmpl_id, option_id"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Producto",
        required=True,
        ondelete="cascade",
    )
    option_id = fields.Many2one(
        comodel_name="product.rented.time.option",
        string="Opción de tiempo",
        required=True,
        ondelete="restrict",
    )
    base_price = fields.Float(string="Precio base", required=True)
    discount_percent = fields.Float(string="% Descuento", default=0.0)
    final_price = fields.Float(
        string="Precio final",
        compute="_compute_final_price",
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        (
            "product_option_unique",
            "unique(product_tmpl_id, option_id)",
            "Cada opción de tiempo solo puede tener un precio por producto.",
        )
    ]

    @api.depends("base_price", "discount_percent")
    def _compute_final_price(self):
        for record in self:
            discount_factor = 1.0 - (record.discount_percent or 0.0) / 100.0
            record.final_price = record.base_price * max(discount_factor, 0.0)
