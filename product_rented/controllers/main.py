from odoo import http
from odoo.http import request


class RentedProductController(http.Controller):

    @http.route(['/rented_product'], type='http', auth='public', website=True, sitemap=False)
    def render_rented_products_page(self, **kwargs):
        
        rented_products = request.env['product.template'].sudo().search([
            ('rented_bolean', '=', True),
            ('website_published', '=', True),
        ])
        values = {
            'products': rented_products,
        }
        return request.render('product_rented.template_product_rented', values)
