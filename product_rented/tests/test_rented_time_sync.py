from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRentedTimeSync(TransactionCase):

    def setUp(self):
        super().setUp()
        self.option_model = self.env['product.rented.time.option']
        self.option_a = self.option_model.create({
            'name': '1 día',
            'code': '1d',
        })
        self.option_b = self.option_model.create({
            'name': '2 días',
            'code': '2d',
        })
        self.uom_unit = self.env.ref('uom.product_uom_unit')

        self.product = self.env['product.template'].create({
            'name': 'Producto de renta',
            'type': 'consu',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'rented_time_option_ids': [(6, 0, [self.option_a.id])],
            'rented_time_price_ids': [
                (0, 0, {
                    'option_id': self.option_a.id,
                    'base_price': 100.0,
                })
            ],
        })

    def test_constraint_prevents_inconsistent_configuration(self):
        with self.assertRaises(ValidationError):
            self.product.write({
                'rented_time_option_ids': [(6, 0, [self.option_a.id, self.option_b.id])],
            })

        with self.assertRaises(ValidationError):
            self.product.write({
                'rented_time_option_ids': [(6, 0, [])],
            })

    def test_price_line_changes_sync_allowed_options(self):
        self.product.write({
            'rented_time_price_ids': [
                (0, 0, {
                    'option_id': self.option_b.id,
                    'base_price': 120.0,
                })
            ],
        })
        self.assertEqual(
            set(self.product.rented_time_option_ids.ids),
            {self.option_a.id, self.option_b.id},
        )

        line_to_remove = self.product.rented_time_price_ids.filtered(
            lambda line: line.option_id == self.option_a
        )
        line_to_remove.ensure_one()
        self.product.write({
            'rented_time_price_ids': [(2, line_to_remove.id, 0)],
        })
        self.assertEqual(
            set(self.product.rented_time_option_ids.ids),
            {self.option_b.id},
        )
