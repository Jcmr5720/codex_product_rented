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
        time_price_details = {}
        for product in rented_products:
            if product.rented_price and product.currency_id:
                formatted_prices[product.id] = tools.format_amount(
                    request.env, product.rented_price, product.currency_id
                )
            else:
                formatted_prices[product.id] = False

            details = []
            for time_price in product.rented_time_price_ids:
                option_name = (
                    time_price.option_id.display_name
                    or time_price.option_id.name
                    or ""
                )
                final_price = time_price.final_price
                has_price = final_price not in (None, False)
                if has_price and product.currency_id:
                    formatted_rate = tools.format_amount(
                        request.env, final_price, product.currency_id
                    )
                else:
                    formatted_rate = False
                details.append(
                    {
                        "id": time_price.id,
                        "option_name": option_name,
                        "option_code": (time_price.option_id.code or "").lower(),
                        "formatted_price": formatted_rate,
                        "has_price": has_price,
                        "raw_price": final_price,
                    }
                )
            time_price_details[product.id] = details
        values = {
            'products': rented_products,
            'formatted_rented_prices': formatted_prices,
            'time_price_details': time_price_details,
        }
        return request.render('product_rented.template_product_rented', values)
