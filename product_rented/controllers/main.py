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
        product_ui_meta = {}
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

            badge_featured = bool(getattr(product, "rented_is_featured", False))
            badge_new = bool(
                getattr(product, "rented_is_new", False)
                or getattr(product, "is_new", False)
            )
            badge_promo = bool(
                getattr(product, "rented_is_on_promotion", False)
                or getattr(product, "rented_is_promo", False)
                or getattr(product, "is_promo", False)
                or getattr(product, "rented_is_promotional", False)
            )
            quote_url = (
                getattr(product, "rented_quote_url", False)
                or "/contactus?subject=Solicitud%20de%20cotizaci%C3%B3n&product_id=%s"
                % product.id
            )

            product_ui_meta[product.id] = {
                "badge_featured": badge_featured,
                "badge_new": badge_new,
                "badge_promo": badge_promo,
                "quote_url": quote_url,
            }
        values = {
            'products': rented_products,
            'formatted_rented_prices': formatted_prices,
            'time_price_details': time_price_details,
            'product_ui_meta': product_ui_meta,
        }
        return request.render('product_rented.template_product_rented', values)
