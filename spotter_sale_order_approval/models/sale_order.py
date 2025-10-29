from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    choose_currency_id = fields.Many2one("res.currency",string="Currency")

    exchange_rate = fields.Monetary(string="Exchange Range", compute="compute_exchange_rate", store=True)

    symbol = fields.Char()

    @api.depends('choose_currency_id.rate_ids')
    def compute_exchange_rate(self):


        amount_to_convert = self.amount_total
        from_currency = self.currency_id
        to_currency = self.choose_currency_id
        converted_amount = from_currency._convert(
            amount_to_convert,
            to_currency,
            self.env.company,
            fields.Date.today()
        )
        self.exchange_rate =converted_amount
        print("helo")


















    # currency_id = fields.Many2one('res.currency', string="Currency",
    #                               related='company_id.currency_id',
    #                               default=lambda
    #                                   self: self.env.user.company_id.currency_id.id)
    #
    # state = fields.Selection(
    #     selection_add=[
    #         ('to_approve', 'To Approve')
    #     ]
    # )

    # def action_confirm(self):
    #     print("self.amount_total", self.amount_total)
    #
    #
    #     self.write({'state':'to_approve'})
    #
    #     if not self.env.user.has_group(
    #             'base.group_purchase_manager'):
    #         raise UserError('You cannot archive service')
    #     # raise ValidationError("asdfghjkjhgf")
    #     return super(SaleOrder, self).action_confirm()
