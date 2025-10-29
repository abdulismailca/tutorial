from odoo import api, fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'


    account_move_id = fields.Many2one('account.move', string='Sale Order', readonly=True)

    def add_invoice_line(self):
        print("button clicked")




        print("clicked line", self.product_id.name)
        print("clicked line", )
        for rec in self.move_id.invoice_line_ids:
            print("rec", rec.product_id.name)
            print("rec", rec.quantity)





