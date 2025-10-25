from odoo import models,fields,api
from odoo.exceptions import UserError



class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[('multisafepay', "Multisafepay")], ondelete={'multisafepay': 'set default'}
    )

    multisafepay_api_key_test = fields.Char('MultiSafepay test api key', size=40)

    @api.onchange('multisafepay_api_key_test')
    def _onchange_multisafepay_api_key_test(self):
        if self.multisafepay_api_key_test and len(self.multisafepay_api_key_test) != 40:
            raise UserError('An API key must be 40 characters long')




