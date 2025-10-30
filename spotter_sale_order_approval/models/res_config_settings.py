from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    crm_message_limit = fields.Integer(string="Time Limit",  config_parameter="spotter_sale_order_approvl.crm_message_limit")

