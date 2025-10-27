from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_prime_customer = fields.Boolean(string="Is Prime Customer")