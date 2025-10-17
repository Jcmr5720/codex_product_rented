from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

class rentedProduct(Website):
        
    @http.route('/rented_product', type='http', auth='public', website=True, sitemap=False)
    def pages(self, **kw):
        rented_products = request.env['product.template'].sudo().search([
            ('rented_bolean', '=', True),
            ('website_published', '=', True),
        ])
        values = {'products': rented_products}
        return request.render('product_rented.template_product_rented', values)
