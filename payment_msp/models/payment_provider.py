# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug import urls

from odoo import _, fields, models, service
from odoo.exceptions import ValidationError

from odoo.addons.payment_mollie import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'Multisafepay')],
        ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char(
        string="Multisafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay", groups="base.group_system"
    )

    #=== BUSINESS METHODS ===#

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'multisafepay':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies

    def _multisafepay_make_request(self,data=None, method='POST'):

        print("iam from _multisafepay_make_request")
        self.ensure_one()
        url = f"https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafepay_api_key}"

        # url = "https://testapi.multisafepay.com/v1/json/orders?api_key=7caeed9a6b8e4efff21a9b8a9e6a51f274f0cb3c"



        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)



        return response

        try:
            print("iam from try block")

            response = requests.post(url, json=data, headers=headers)
            print("Response",response.text)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url,
                    pprint.pformat(data)
                )
                raise ValidationError(
                    "Multisafepay: " + _(
                        "The communication with the API failed. MultisafePay gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):

            print("iam from exception")
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Multisafepay: " + _(
                    "Could not establish the connection to the API.")
            )
        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'multisafepay':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES

