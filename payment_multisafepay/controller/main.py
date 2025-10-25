import logging
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, _logger
from odoo.http import Response
import requests


class MultisafePayController(http.Controller):
    _return_url='/payment/multisafepay/return'
    _cancel_url='/payment/multisafepay/cancel'
    # _webhook_url='/payment/multisafepay/webhook/'

    @http.route('/payment/multisafepay/return', type='http', auth='public', csrf=False)
    def multisafepay_return(self, **kwargs):
        print(kwargs)
        _logger.info("MultiSafepay Return Params: %s", kwargs)


        reference = kwargs.get("transactionid") or kwargs.get("order_id")


        if not reference:
            return request.redirect('/payment/status?error=missing_reference')

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
        if not tx:
            return request.redirect('/payment/status?error=transaction_not_found')

        provider_ref = kwargs.get("session_id")
        if provider_ref:
            tx.write({'provider_reference': provider_ref})

        tx.process_multisafepay_notification(reference)
        return request.redirect('/payment/status')

    @http.route(_cancel_url, type='http', auth='public', csrf=False)
    def multisafepay_cancel(self, **kwargs):
        # print("gelljjjmn")
        _logger.info("MultiSafepay Cancel Params: %s", kwargs)

        reference = kwargs.get("transactionid") or kwargs.get("order_id")
        # print("red",reference)


        if reference:
            tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
            print("kkkk",tx)
            if tx:
                tx._set_canceled()
        return request.redirect('/payment/status?canceled=1')

    @http.route('/payment/multisafepay/webhook', type='json', auth='public', csrf=False)
    def multisafepay_webhook(self, **kwargs):
        print("klkllk")
        _logger.info("MultiSafepay Webhook Data: %s", kwargs)

        reference = kwargs.get("transactionid") or kwargs.get("order_id")
        if not reference:
            return {"status": "error", "reason": "missing_reference"}

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
        if not tx:
            return {"status": "error", "reason": "transaction_not_found"}

        tx.process_multisafepay_notification(reference)
        return {"status": "ok"}










