from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'


    all_invoice_lines_ids = fields.One2many('account.move.line','account_move_id', compute="compute_all_invoice_lines")



    def compute_all_invoice_lines(self):

        all_invoice_line = self.invoice_line_ids.search([], limit=20)
        self.all_invoice_lines_ids = all_invoice_line

    def add_invoice_line(self):
        pass




