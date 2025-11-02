from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    approver_1_id = fields.Many2one("res.users", string="Approver 1", help="First approver", config_parameter="so_purchase_limit.approver_1_id")
    approver_2_id = fields.Many2one("res.users", string="Approver 2", help="Second approver", config_parameter="so_purchase_limit.approver_2_id")

