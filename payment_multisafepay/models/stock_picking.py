from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):

        for line in self.move_line_ids:
            if line.expiration_date:
                if line.expiration_date.date() < date.today():
                    print(line.product_id.name)
                    raise UserError(f"Expired Product Found")





        return super(StockPicking, self).button_validate()
