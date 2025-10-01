from odoo import fields, models



class PosPurchaseLimit(models.Model):
    _inherit = "res.partner"

    is_activate_purchase_limit = fields.Boolean(string="Activate Purchase Limit")
    purchase_limit = fields.Integer(string="Purchase Limit")

    def _load_pos_data_fields(self, config_id):


        fields = super()._load_pos_data_fields(config_id)
        fields.append('is_activate_purchase_limit,purchase_limit')
        return fields