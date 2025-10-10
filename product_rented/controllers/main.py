from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.exceptions import AccessError
from werkzeug.exceptions import NotFound

import logging

_logger = logging.getLogger(__name__)

class rentedProduct(Website):
        
    @http.route('/rented_product', type='http', auth='public', website=True, sitemap=False)
    def pages(self, **kw):
        return request.render('product_rented.template_product_rented', values)