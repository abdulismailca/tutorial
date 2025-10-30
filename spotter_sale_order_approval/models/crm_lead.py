from datetime import date, datetime, timedelta

from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    last_chatter_message_time = fields.Datetime(string="Last Chatter Message",
                                                compute='compute_last_chatter_message_time',
                                                store=True)

    message_limit = fields.Integer()

    @api.depends('message_ids')
    def compute_last_chatter_message_time(self):
        for record in self:
            last_message = self.env['mail.message'].search([
                ('res_id', '=', record.id),
                ('model', '=', 'crm.lead'),

            ], order='create_date desc', limit=1)
            record.last_chatter_message_time = last_message.create_date if last_message else False

            print("helo")
            record.message_limit = record.env[
                'ir.config_parameter'].sudo().get_param(
                'spotter_sale_order_approvl.crm_message_limit')

            print("record.message_limit", record.message_limit)
            print("record.last_chatter_message_time",
                  record.last_chatter_message_time)

            time_now = datetime.today()
            print("time_now", time_now)

            diff = record.last_chatter_message_time - time_now

            difference_in_minutes = abs(diff.total_seconds()) / 60


            if difference_in_minutes < record.message_limit:

                self.action_archive()
            #
            # if record.message_limit:
            #     self.action_archive()
            print("message_limit", record.message_limit)
