from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_product_template_fields(self):
        result = super()._get_pos_ui_product_template_fields()
        result.append('quality_rating')
        return result
