# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment.const import CURRENCY_MINOR_UNITS

from odoo.http import request
from .. import const

from ..controllers.main import MultisafePay





_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'



    def _get_specific_rendering_values(self, processing_values):
        print("ismail , did you see the rizq")
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res





        payload = self._multisafepay_prepare_payment_request_payload()
        payment_data = self.provider_id._multisafepay_make_request(data=payload)

        response_data = payment_data.json()
        print("response_data", response_data)

        payment_url = response_data["data"]["payment_url"]
        print("payment_url:", payment_url)

        return {'api_url': payment_url}

        # # The provider reference is set now to allow fetching the payment status after redirection
        # self.provider_reference = payment_data.get('id')
        #
        #
        # checkout_url = payment_data['_links']['checkout']['href']
        # parsed_url = urls.url_parse(checkout_url)
        # url_params = urls.url_decode(parsed_url.query)
        # return {'api_url': checkout_url, 'url_params': url_params}

    def _multisafepay_prepare_payment_request_payload(self):



        base_url = self.provider_id.get_base_url()
        user_lang = self.env.context.get('lang')
        print(user_lang)
        decimal_places = CURRENCY_MINOR_UNITS.get(
            self.currency_id.name, self.currency_id.decimal_places
        )

        print(decimal_places)


        amount_to_pay = f"{self.amount:.{decimal_places}f}"
        amount_cents = int(round(float(amount_to_pay) * 100))
        print(amount_cents)


        print(amount_to_pay)


        notification_url = urls.url_join(base_url,'/payment/multisafepay/webhook')
        redirect_url = urls.url_join(base_url, '/payment/multisafepay/return')
        cancel_url = urls.url_join(base_url, '/payment/multisafepay/return')

        payload = {
            "payment_options": {
                "close_window": True,
                "notification_method": "POST",
                "notification_url": notification_url,
                "redirect_url": redirect_url,
                "cancel_url": cancel_url,
            },
            "customer": {
                "locale": user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            "type": "redirect",
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": amount_cents,
            "description": "Test Order Description"
        }

        return payload




    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Mollie data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'mollie' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('ref')), ('provider_code', '=', 'mollie')]
        )
        if not tx:
            raise ValidationError("Mollie: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return

        payment_data = self.provider_id._mollie_make_request(
            f'/payments/{self.provider_reference}', method="GET"
        )

        # Update the payment method.
        payment_method_type = payment_data.get('method', '')
        if payment_method_type == 'creditcard':
            payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        payment_method = self.env['payment.method']._get_from_code(
            payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        )
        self.payment_method_id = payment_method or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('status')
        if payment_status in ('pending', 'open'):
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'paid':
            self._set_done()
        elif payment_status in ['expired', 'canceled', 'failed']:
            self._set_canceled("Mollie: " + _("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Mollie: " + _("Received data with invalid payment status: %s", payment_status)
            )
