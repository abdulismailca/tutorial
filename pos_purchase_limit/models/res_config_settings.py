from odoo import api, fields, models
class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'

    is_activate_purchase_limit_res_settings = fields.Boolean(
        string="Activate Purchase Limit")

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()

        is_activate_purchase_limit_res_settings = icp_sudo.get_param('res.config.settings.is_activate_purchase_limit_res_settings')

        res.update(
           is_activate_purchase_limit_res_settings = is_activate_purchase_limit_res_settings
        )
        return res
    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.is_activate_purchase_limit_res_settings', self.is_activate_purchase_limit_res_settings)

        return res

