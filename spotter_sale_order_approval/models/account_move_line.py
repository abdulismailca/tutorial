from odoo import api, fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    account_move_id = fields.Many2one('account.move', string='Sale Order', readonly=True)

    def add_invoice_line(self):
        pass