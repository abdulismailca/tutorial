from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False):

        quantity = quantity or 0.0

        product = self
        sellers = product.seller_ids.filtered(lambda s: not s.company_id or s.company_id == product.env.company)

        valid_sellers = []
        for seller in sellers:
            if date and ((seller.date_start and seller.date_start > date) or (seller.date_end and seller.date_end < date)):
                continue
            if seller.min_qty and quantity < seller.min_qty:
                continue
            valid_sellers.append(seller)

        if not valid_sellers:
            return super(ProductProduct, self)._select_seller(partner_id, quantity, date, uom_id, params)

        def compute_price(seller):
            price = seller.price
            if uom_id and seller.product_uom and seller.product_uom != uom_id:
                price = seller.product_uom._compute_price(price, uom_id)
            return price

        valid_sellers.sort(key=lambda s: (compute_price(s), s.delay))
        return valid_sellers[0]
