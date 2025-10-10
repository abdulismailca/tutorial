from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):

        # expiration_time

        # print("Move line",self.move_line_ids)
        print("move ids",self.move_ids)
        # print("Move line", self.product_id)
        if self.move_ids:
            if self.move_ids.use_expiration_date:
                # today = date.today()
                for rec in self.move_ids:

                    if self.move_ids.expiration_time < date.today():
                        raise UserError("Expire Product Found!")


        return super(StockPicking, self).button_validate()
