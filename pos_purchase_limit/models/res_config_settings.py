from odoo import  fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_activate_purchase_limit_res_settings = fields.Boolean(string="Activate Purchase Limit")





