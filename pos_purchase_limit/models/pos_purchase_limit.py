from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_activate_purchase_limit = fields.Boolean(string="Activate Purchase Limit", compute='_compute_my_config_value')
    purchase_limit = fields.Integer(string="Purchase Limit Amount")

    @api.onchange('purchase_limit')
    def purchase_limit_validation(self):
        print("work properly")
        if self.purchase_limit <= 0:

            raise UserError('Purchase Limit Must be Greater than Zero!')

    @api.depends()
    def _compute_my_config_value(self):
        icp_sudo = self.env['ir.config_parameter'].sudo()
        is_limit_active = icp_sudo.get_param(
            'res.config.settings.is_activate_purchase_limit_res_settings')

        print("is_limit_active", is_limit_active)

        for record in self:
            if not is_limit_active:

                record.is_activate_purchase_limit = False
                print("fields", record.is_activate_purchase_limit)
            else:

                record.is_activate_purchase_limit = True
                print("fields", record.is_activate_purchase_limit)


    def _load_pos_data_fields(self, config_id):

        fields = super()._load_pos_data_fields(config_id)
        fields.extend(['is_activate_purchase_limit', 'purchase_limit'])
        return fields
