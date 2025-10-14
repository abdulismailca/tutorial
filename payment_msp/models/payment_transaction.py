# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import re

import requests
from docutils.nodes import reference
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






        # The provider reference is set now to allow fetching the payment status after redirection


        response_data = payment_data.json()
        self.provider_reference = response_data.get('provider_id')
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

        # payload = self._multisafepay_prepare_payment_request_payload()
        # payment_data = self.provider_id._multisafepay_make_request(data=payload)
        #
        # print("payload from tx",payment_data.json())
        # msp_reference = payload.get('order_id')

        #ivide reference cut akkendi varum enna thonunne.

        print("notification ann",notification_data.get('transactionid'))
        msp_reference = notification_data.get('transactionid')

        parts = re.split(r"[-]", msp_reference)
        real_msp_reference = parts[0]

        print("parts",parts)

        tx = self.search(
            [('reference', '=',real_msp_reference), ('provider_code', '=', 'multisafepay')]
        )

        print("tx",tx)
        if not tx:
            raise ValidationError("Multisafpay: " + _(
                "No transaction found matching reference %s.", notification_data.get('transactionid')
            ))
        return tx


    def _multisafepay_status_update(self,url):

        print("hi iam from _multisafepay_status_update")
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        return response


    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return


        msp_reference = notification_data.get('transactionid')

        url = f"https://testapi.multisafepay.com/v1/json/orders/{self.reference}?api_key={self.provider_id.multisafepay_api_key}"

        print("URL with api",url)

        headers = {"accept": "application/json"}

        response = self._multisafepay_status_update(url)

        paymnet_data = response.json()



        payment_transaction_id = paymnet_data['data'].get('transaction_id')









        url = f'https://testapi.multisafepay.com/v1/json/transactions/{payment_transaction_id}?api_key={self.provider_id.multisafepay_api_key}'

        headers = {"accept": "application/json"}
        transaction_response = requests.get(url, headers=headers).json()



        payment_status = transaction_response['data'].get('status')




        if payment_status in ['pending','approved']:
            self._set_pending()
            print("ia from first if")

        elif payment_status in ['completed']:
            self._set_done()
            print("iam from second elif")
        elif payment_status in ['canceled','declined', 'initialized']:

            print("iam from thired elif")



            self._set_canceled("Multisafepay: " + _("Cancelled payment with status: %s", payment_status))
        else:
            print("iam from else")
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status,msp_reference
            )
            self._set_error(
                "Multisafepay: " + _("Received data with invalid payment status: %s", payment_status)
            )
