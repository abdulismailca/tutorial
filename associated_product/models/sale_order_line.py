from odoo import fields, models


class SalseOrderLine(models.Model):
    _inherit = 'sale.order.line'


    partner_id = fields.Many2one('res.partner', string="Partner ID")