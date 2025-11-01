from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _prepare_sellers(self, params=False):
        sellers = super()._prepare_sellers()
        return sellers.sorted(lambda s: (s.price, s.delay))
