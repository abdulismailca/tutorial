from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    multiple_invoice_id = fields.Many2one('account.move')