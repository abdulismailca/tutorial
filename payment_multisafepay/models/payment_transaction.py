import logging

from odoo import models,fields,_,api
from werkzeug import urls
import requests

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_aps import utils as aps_utils
from odoo.addons.payment_aps.controllers.main import APSController

from odoo.addons.test_convert.tests.test_env import data
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import json

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    # provider_reference = fields.Char(string="Provider Reference")

    def _get_specific_rendering_values(self, processing_values):
        self.ensure_one()
        # print("helloooo")
        res = super()._get_specific_rendering_values(processing_values)

        if self.provider_code != 'multisafepay':
            return res

        base_url = self.provider_id.get_base_url()


        values = {
            "type": "redirect",
        "gateway": "IDEAL",
        "order_id": self.reference,
        "currency": self.currency_id.name,
        "amount": int(self.amount * 100),
        "description": "Test Order Description",
                       "payment_options": {
                           "redirect_url": f"{base_url}/payment/multisafepay/return",
                           "cancel_url": f"{base_url}/payment/multisafepay/cancel",
                           "notification_method": "POST",
                           "notification_url": f"{base_url}/payment/multisafepay/webhook",

                       },
                       "customer": {
                           "email": self.partner_email or "",
                           "locale": self.partner_id.lang or 'it_IT',
                       }
                   }
        headers = {
            'Accept': "application/json",
            "Content-type": "application/json"
        }
        api_url = f"https://testapi.multisafepay.com/v1/json/orders?api_key={self.provider_id.multisafepay_api_key_test}"
        response = requests.post(api_url, headers=headers, data=json.dumps(values))
        print(response)
        try:
            payment_data = response.json()
            print("prov.ref",payment_data)
        except Exception:
            payment_data = {"error": "Invalid JSON response", "text": response.text}

        logging.info("MultiSafepay Response: %s", payment_data)
        return {
            'api_url': payment_data.get("data", {}).get("payment_url", ""),
        }

    def process_multisafepay_notification(self, reference):
        print("inside noti")
        self.ensure_one()


        api_url = f"https://testapi.multisafepay.com/v1/json/orders/{reference}?api_key={self.provider_id.multisafepay_api_key_test}"
        response = requests.get(api_url)
        try:
            result = response.json()
        except Exception:
            _logger.error("Invalid JSON from MultiSafepay: %s", response.text)
            return False


        status = result.get("data", {}).get("status")
        _logger.info("MultiSafepay Status for %s: %s", reference, status)

        if status == "completed":
            self._set_done()
        elif status == "cancelled":
            self._set_canceled()
        elif status == "expired":
            self._set_error("Payment expired")
        else:
            self._set_pending()

        return True

