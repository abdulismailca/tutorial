from datetime import timedelta, datetime
from email.policy import default

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_move_count = fields.Integer(string="Move Count",
                                      compute='compute_stock_move_count')

    def compute_stock_move_count(self):
        today = datetime.now()
        seven_days_ago = today - timedelta(days=7)
        date_from = seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        date_to = today.strftime('%Y-%m-%d %H:%M:%S')

        all_moves = self.env['stock.move'].search(
            [('product_id', '=', self.id), ('create_date', '>=', date_from),
             ('create_date', '<=', date_to)])

        # all_moves_filtered = all_moves.filtered(lambda s: s.create_date < timedelta)
        print("s",all_moves)

        self.write({'stock_move_count': len(all_moves)})
