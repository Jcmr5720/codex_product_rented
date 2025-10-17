from odoo import http, tools
from odoo.http import request


class RentedProductController(http.Controller):

    @http.route(['/rented_product'], type='http', auth='public', website=True, sitemap=False)
    def render_rented_products_page(self, **kwargs):
        
        rented_products = request.env['product.template'].sudo().search([
            ('rented_bolean', '=', True),
            ('website_published', '=', True),
        ])
        formatted_prices = {}
        for product in rented_products:
            if product.rented_price and product.currency_id:
                formatted_prices[product.id] = tools.format_amount(
                    request.env, product.rented_price, product.currency_id
                )
            else:
                formatted_prices[product.id] = False
        values = {
            'products': rented_products,
            'formatted_rented_prices': formatted_prices,
        }
        return request.render('product_rented.template_product_rented', values)
