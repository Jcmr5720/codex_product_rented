from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented_bolean = fields.Boolean(string="Puede ser rentado")
    rented_prince = fields.Float(string="Precio de renta")
    rented_time = fields.Char(string="Tiempo de renta")
    rented_description = fields.Text(string="Descripción de renta")
    rented_profit = fields.Float(string="Ganancia de renta")
