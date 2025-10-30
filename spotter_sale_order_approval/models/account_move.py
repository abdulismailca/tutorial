from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    my_invoice_ids = fields.Many2many("my.invoice.line", "my_invoice_id",compute="compute_all_invoice_lines")

    @api.depends('partner_id')
    def compute_all_invoice_lines(self):
        for rec in self:
            all_invoice_line = rec.invoice_line_ids.search(
                [('product_id', '!=', False)], order='create_date', limit=20)

            print("all_invoice_line", all_invoice_line)

            rec.my_invoice_ids = [(fields.Command.clear())]

            rec.my_invoice_ids = [(fields.Command.create({
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'my_invoice_id': rec.id

            })) for line in all_invoice_line]

        print("end of the line")

    def add_all_invoice_line(self):

        all_invoice_line = self.my_invoice_ids.search([], order='create_date',
                                                     limit=20)

        print("all_invoice_line from button", all_invoice_line)

        self.invoice_line_ids = [(fields.Command.create({
            'product_id': line.product_id.id,
            'quantity': line.quantity,
            'price_unit': line.price_unit,
            'price_subtotal': line.price_subtotal,
            'move_id': self.id

        })) for line in all_invoice_line]

        self.my_invoice_ids = [(fields.Command.clear())]


        print("end of the line")

    def action_post(self):
        raise ValidationError("dfghj")
