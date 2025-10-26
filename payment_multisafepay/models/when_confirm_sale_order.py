from datetime import date, datetime

from odoo import fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        his_sale_order =self.partner_id.sale_order_ids

        confirm_sale_order = his_sale_order.filtered(lambda s: s.state =="sale")

        his_total_po_amount = confirm_sale_order.mapped('amount_total')

        his_po_sum = sum(his_total_po_amount)




        # today = datetime.now()
        six_months = datetime.now() - relativedelta(months=+6)

        print("before six month", six_months)

        his_six_month_po = confirm_sale_order.filtered(lambda s: s.date_order <= six_months)

        count_his_six_month_po = len(his_six_month_po)

        print("before six month order", his_six_month_po)











        len_confirm_sale_order = len(confirm_sale_order)
        if len_confirm_sale_order < 2 or his_po_sum > 10000 or count_his_six_month_po>=1:
            raise UserError("at leat minimum 2 sale order need")






        return super(SaleOrder, self).action_confirm()

