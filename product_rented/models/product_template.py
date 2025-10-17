from odoo import api, fields, models
from odoo.exceptions import ValidationError


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

    @staticmethod
    def _collect_price_line_option_ids(lines):
        return {line.option_id.id for line in lines if line.option_id}

    def _get_price_line_option_ids(self):
        self.ensure_one()
        return sorted(self._collect_price_line_option_ids(self.rented_time_price_ids))

    @api.onchange("rented_time_price_ids")
    def _onchange_rented_time_price_ids(self):
        for product in self:
            option_ids = product._get_price_line_option_ids()
            product.rented_time_option_ids = [(6, 0, option_ids)]

    @api.model
    def _compute_synced_option_ids(self, price_commands, existing_lines=None):
        existing_lines = existing_lines or self.env["product.rented.time.price"]
        option_ids = set(self._collect_price_line_option_ids(existing_lines))
        lines_by_id = {line.id: line for line in existing_lines}

        for command in price_commands or []:
            if not command:
                continue
            command_type = command[0]

            if command_type == 0:
                data = command[2] or {}
                option_id = data.get("option_id")
                if option_id:
                    option_ids.add(option_id)
            elif command_type == 1:
                line_id = command[1]
                data = command[2] or {}
                line = lines_by_id.get(line_id)
                if "option_id" in data:
                    if line and line.option_id:
                        option_ids.discard(line.option_id.id)
                    new_option_id = data.get("option_id")
                    if new_option_id:
                        option_ids.add(new_option_id)
            elif command_type in (2, 3):
                line_id = command[1]
                line = lines_by_id.get(line_id)
                if line and line.option_id:
                    option_ids.discard(line.option_id.id)
            elif command_type == 4:
                line_id = command[1]
                line = self.env["product.rented.time.price"].browse(line_id)
                lines_by_id[line_id] = line
                if line.option_id:
                    option_ids.add(line.option_id.id)
            elif command_type == 5:
                option_ids.clear()
            elif command_type == 6:
                record_ids = command[2] or []
                records = self.env["product.rented.time.price"].browse(record_ids)
                lines_by_id = {line.id: line for line in records}
                option_ids = set(self._collect_price_line_option_ids(records))

        return sorted(option_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "rented_time_price_ids" in vals:
                synced_option_ids = self._compute_synced_option_ids(vals.get("rented_time_price_ids"))
                vals["rented_time_option_ids"] = [(6, 0, synced_option_ids)]
        return super().create(vals_list)

    def write(self, vals):
        if "rented_time_price_ids" in vals:
            price_commands = vals.get("rented_time_price_ids")
            for product in self:
                synced_option_ids = product._compute_synced_option_ids(
                    price_commands, existing_lines=product.rented_time_price_ids
                )
                product_vals = dict(vals)
                product_vals["rented_time_option_ids"] = [(6, 0, synced_option_ids)]
                super(ProductTemplate, product).write(product_vals)
            return True
        return super().write(vals)

    @api.constrains("rented_time_option_ids", "rented_time_price_ids.option_id")
    def _check_rented_time_options_prices(self):
        for product in self:
            option_ids = set(product.rented_time_option_ids.ids)
            price_lines = product.rented_time_price_ids
            line_option_ids = [line.option_id.id for line in price_lines if line.option_id]
            line_option_set = set(line_option_ids)
            duplicates = len(line_option_ids) != len(line_option_set)

            missing_prices = option_ids - line_option_set
            disallowed_lines = line_option_set - option_ids

            if missing_prices:
                missing_names = product.rented_time_option_ids.filtered(
                    lambda option: option.id in missing_prices
                ).mapped("name")
                raise ValidationError(
                    "Cada opción de tiempo seleccionada debe tener exactamente una tarifa definida. "
                    "Faltan precios para: %s" % ", ".join(missing_names)
                )

            if disallowed_lines:
                disallowed_names = price_lines.filtered(
                    lambda line: line.option_id.id in disallowed_lines
                ).mapped("option_id.name")
                raise ValidationError(
                    "Las tarifas de renta solo pueden usar opciones permitidas. "
                    "Revise: %s" % ", ".join(disallowed_names)
                )

            if duplicates:
                raise ValidationError(
                    "Cada opción de tiempo solo puede tener una tarifa configurada por producto."
                )
