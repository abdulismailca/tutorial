from odoo import fields, models

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    is_prime_customer = fields.Boolean(string="Is Prime Customer",  related='partner_id.is_prime_customer')

