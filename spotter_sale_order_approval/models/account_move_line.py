from odoo import api, fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'


    account_move_id = fields.Many2one('account.move', string='Invoice Id', readonly=True)









