from odoo import http
from odoo.http import request

class WebsiteProduct(http.Controller):
    @http.route('/clear/cart', type='http',
                auth="user", website=True)
    def clear_cart(self, **kw):
        print("Yes you are near on clear cart")

        order = request.website.sale_get_order()


        print("what is this", order.name)
        order.unlink()
        return request.redirect('/shop/cart')








