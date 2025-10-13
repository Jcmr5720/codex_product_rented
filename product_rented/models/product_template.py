from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented_bolean = fields.Boolean(string="Puede ser rentado")
    rented_price = fields.Float(string="Precio de renta", oldname="rented_prince")
    rented_time = fields.Selection(
        [
            ("1m", "1 mes"),
            ("2m", "2 meses"),
            ("3m", "3 meses"),
            ("6m", "6 meses"),
            ("1y", "1 año"),
            ("2y", "2 años"),
        ],
        string="Tiempo de renta",
    )
    rented_description = fields.Text(string="Descripción de renta")
    rented_profit = fields.Float(string="Ganancia de renta")
