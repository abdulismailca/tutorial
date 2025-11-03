from odoo import fields, models, api



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    res_partner_id = fields.Many2one('res.partner')