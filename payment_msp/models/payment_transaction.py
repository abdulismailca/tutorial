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


        notification_url = urls.url_join(base_url,MultisafePay._webhook_url)
        redirect_url = urls.url_join(base_url,MultisafePay._return_url)
        cancel_url = urls.url_join(base_url,MultisafePay._return_url)

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

        print("iam from _get_tx_from_notification_data")
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx

        print("notification",notification_data)

        payload = self._multisafepay_prepare_payment_request_payload()
        print("payload from tx",payload)
        msp_reference = payload.get('order_id')

        #ivide reference cut akkendi varum enna thonunne.

        tx = self.search(
            [('reference', '=',msp_reference), ('provider_code', '=', 'multisafepay')]
        )

        print("tx",tx)
        if not tx:
            raise ValidationError("Multisafpay: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return

        payment_data = self.provider_id._multisafepay_make_request(
            f'/payments/{self.provider_reference}', method="GET"
        )
        print("iam from process notification",payment_data.json())

        # Update the payment method.
        # payment_method_type = payment_data.get('method', '')
        # if payment_method_type == 'creditcard':
        #     payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        # payment_method = self.env['payment.method']._get_from_code(
        #     payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        # )
        # self.payment_method_id = payment_method or self.payment_method_id

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
