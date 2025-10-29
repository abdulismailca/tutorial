from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    all_invoice_lines_ids = fields.Many2many('account.move.line', 'account_move_id',store=True, compute="compute_all_invoice_lines")

    @api.depends('partner_id')

    def compute_all_invoice_lines(self):

        for rec in self:
            all_invoice_line = rec.invoice_line_ids.search(
                [('partner_id', '=', rec.partner_id.id), ('product_id', '!=', False)], order='create_date', limit=20)

            print("all_invoice_line", all_invoice_line)

        # self.all_invoice_lines_ids = [(fields.Command.clear())]

            rec.all_invoice_lines_ids=[(fields.Command.create({
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'account_move_id': rec.id

                })) for line in all_invoice_line]
       
        print("end of the line")
