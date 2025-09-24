from odoo import models, fields

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        print("hey iam here")
        result['search_params']['fields'].append('qty_available')
        return result


