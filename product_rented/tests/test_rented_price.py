# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase


class TestRentedPrice(TransactionCase):
    def setUp(self):
        super().setUp()
        uom_unit = self.env.ref("uom.product_uom_unit")
        self.product_template = self.env["product.template"].create(
            {
                "name": "Camera Pro",
                "type": "service",
                "uom_id": uom_unit.id,
                "uom_po_id": uom_unit.id,
                "rented_bolean": True,
            }
        )
        self.option_daily = self.env["product.rented.time.option"].create(
            {
                "name": "1 día",
                "code": "1d_test",
            }
        )
        self.option_weekly = self.env["product.rented.time.option"].create(
            {
                "name": "1 semana",
                "code": "1w_test",
            }
        )

    def test_rented_price_takes_lowest_final_price(self):
        self.env["product.rented.time.price"].create(
            {
                "product_tmpl_id": self.product_template.id,
                "option_id": self.option_daily.id,
                "base_price": 100.0,
                "discount_percent": 20.0,
            }
        )
        self.env["product.rented.time.price"].create(
            {
                "product_tmpl_id": self.product_template.id,
                "option_id": self.option_weekly.id,
                "base_price": 200.0,
                "discount_percent": 10.0,
            }
        )

        self.product_template.invalidate_cache(fnames=["rented_price"], ids=self.product_template.ids)
        self.assertEqual(self.product_template.rented_price, 80.0)

    def test_rented_price_updates_with_discount_changes(self):
        time_price = self.env["product.rented.time.price"].create(
            {
                "product_tmpl_id": self.product_template.id,
                "option_id": self.option_daily.id,
                "base_price": 150.0,
                "discount_percent": 0.0,
            }
        )
        self.product_template.invalidate_cache(fnames=["rented_price"], ids=self.product_template.ids)
        self.assertEqual(self.product_template.rented_price, 150.0)

        time_price.discount_percent = 50.0
        time_price.invalidate_cache(fnames=["final_price"], ids=time_price.ids)
        self.product_template.invalidate_cache(fnames=["rented_price"], ids=self.product_template.ids)
        self.assertEqual(self.product_template.rented_price, 75.0)

    def test_rented_price_is_zero_without_time_prices(self):
        self.product_template.invalidate_cache(fnames=["rented_price"], ids=self.product_template.ids)
        self.assertEqual(self.product_template.rented_price, 0.0)
