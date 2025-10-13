from odoo import api, fields, models


class ProductRentedTimeOption(models.Model):
    _name = "product.rented.time.option"
    _description = "Opciones de tiempo de renta"
    _order = "sequence, id"

    name = fields.Char(string="Descripción", required=True)
    code = fields.Char(string="Código", required=True)
    sequence = fields.Integer(string="Secuencia", default=10)

    _sql_constraints = [
        ("code_unique", "unique(code)", "El código de la opción de renta debe ser único."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals = dict(vals)
            vals["code"] = vals["code"].strip()
        return super().write(vals)
