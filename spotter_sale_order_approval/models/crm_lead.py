from datetime import date, datetime, timedelta

from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def last_chatter_message_time(self):

        crm_lead = self.search([])
        for record in crm_lead:
            last_message = self.env['mail.message'].search([
                ('res_id', '=', record.id),
                ('model', '=', 'crm.lead'),

            ], order='create_date desc', limit=1)
            last_chatter_message_time = last_message.create_date if last_message else False

            message_limit = record.env[
                'ir.config_parameter'].sudo().get_param(
                'spotter_sale_order_approval.crm_message_limit')

            difference = fields.datetime.now() - last_chatter_message_time
            record.action_archive()
            if  difference > timedelta(minutes=message_limit):
                record.action_archive()
