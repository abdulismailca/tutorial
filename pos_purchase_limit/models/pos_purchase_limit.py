from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_activate_purchase_limit = fields.Boolean(string="Activate Purchase Limit")
    purchase_limit = fields.Integer(string="Purchase Limit Amount")





    def _load_pos_data_fields(self, config_id):

        fields = super()._load_pos_data_fields(config_id)
        fields.extend(['is_activate_purchase_limit', 'purchase_limit'])
        return fields
