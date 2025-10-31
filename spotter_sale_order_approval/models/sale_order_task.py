from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):

        print("self.amount_total", self.amount_total)

        self.order_line._validate_analytic_distribution()
        self.write(self._prepare_confirmation_values())

        action_lunch_rule
        run
        runbuy

        return super(SaleOrder, self).action_confirm()

