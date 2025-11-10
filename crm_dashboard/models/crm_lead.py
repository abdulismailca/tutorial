import calendar

from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self):
        """current user invoices"""
        user_all_invoices = self.env['account.move'].search(
            [('invoice_user_id', '=', self.user_id.id),
             ('state', '=', 'posted')])

        user_all_invoices_amount = sum(
            user_all_invoices.mapped('amount_total_in_currency_signed'))

        company_id = self.env.company

        # campaign_id
        # medium_id
        # source_id

        """current user leads"""
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])

        """win lose ratio"""
        leads_won = len(self.search([('company_id', '=', company_id.id),
                                     ('user_id', '=', self.env.user.id),
                                     ('stage_id.name', '=', 'Won')]))

        leads_lost = len(self.search([('company_id', '=', company_id.id),
                                      ('user_id', '=', self.env.user.id),
                                      ('stage_id.name', '=', 'Lost')]))


        won_los_ration = str(leads_won) + ':' + str(leads_lost)

        """my activity"""

        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        my_lose = user_all_invoices_amount - expected_revenue

        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'currency': currency,
            'user_all_invoices_amount': user_all_invoices_amount,
            'my_lose': my_lose,
            'won_los_ration': won_los_ration,
        }

    @api.model
    def get_activity_list(self):
        crm_lead_activity = self.env['mail.activity'].search(
            [('res_model', '=', 'crm.lead'),
             ('user_id', '=', self.env.user.id)])
        print("crm_lead_activity", crm_lead_activity)

        crm_lead_activity_mapped = crm_lead_activity.mapped('activity_type_id')

        crm_lead_activity_mail = len(crm_lead_activity_mapped.filtered(lambda s: s.name == 'Email'))
        crm_lead_activity_call = len(crm_lead_activity_mapped.filtered(
            lambda s: s.name == 'Call'))
        crm_lead_activity_to_do = len(crm_lead_activity_mapped.filtered(
            lambda s: s.name == 'To-Do'))
        all_activity = [crm_lead_activity_mail, crm_lead_activity_call,
                        crm_lead_activity_to_do]

        print("crm_lead_activity_mail", crm_lead_activity_mail)
        print("crm_lead_activity_call", crm_lead_activity_call)
        print("crm_lead_activity_to_do", crm_lead_activity_to_do)

        print("new function", all_activity)
        return all_activity

    @api.model
    def lead_by_medium(self):
        company_id = self.env.company
        leads_medium = self.search([('company_id', '=', company_id.id),
                                    ('user_id', '=', self.env.user.id),
                                    ('medium_id', '!=', None)])
        for rec in leads_medium:
            print("rec", rec.medium_id.name)
        leads_medium_each = leads_medium.mapped('medium_id')

        leads_medium_phone = len(leads_medium_each.filtered(
            lambda s: s.name == "Phone"))
        leads_medium_email = len(leads_medium_each.filtered(
            lambda s: s.name == "Email"))

        print("leads_medium_email count",leads_medium_email)
        leads_medium_banner = len(leads_medium_each.filtered(
            lambda s: s.name == "Banner"))
        leads_medium_google = len(leads_medium_each.filtered(
            lambda s: s.name == "Google Adwords"))
        leads_medium_direct = len(leads_medium_each.filtered(
            lambda s: s.name == "Direct"))
        leads_medium_website = len(leads_medium_each.filtered(
            lambda s: s.name == "Website"))

        all_medium_lead_medium_list = [leads_medium_phone, leads_medium_email,leads_medium_banner, leads_medium_google, leads_medium_direct, leads_medium_website]
        print("all_medium_lead_medium_list", all_medium_lead_medium_list)

        return all_medium_lead_medium_list

    # @api.model
    # def lead_by_month_table(self):
    #
    #     company_id = self.env.company
    #     # leads = self.search([('company_id', '=', company_id.id),
    #     #                      ('user_id', '=', self.env.user.id)])
    #
    #     domain = [('create_date', '!=', False),('company_id', '=',company_id.id)]
    #     fields = ['create_date:month', 'id:count']
    #     leads_grouped = self.env['crm.lead'].read_group(
    #
    #         domain,
    #         fields,
    #         ['create_date:month'],
    #         orderby='create_date:month'
    #     )
    #
    #     for group in leads_grouped:
    #         month_year = group['create_date:month']
    #         lead_count = group['id_count']
    #         print(f"Month: {month_year}, Leads Count: {lead_count}")
    #
    #     # return leads_grouped

    @api.model
    def lead_by_month_table(self):
        month_count = []
        month_value = []
        for rec in self.search([]):
            month = rec.create_date.month
            if month not in month_value:
                month_value.append(month)
            month_count.append(month)
        month_val = [{'label': calendar.month_name[month],
                      'value': month_count.count(month)} for month in
                     month_value]
        names = [record['label'] for record in month_val]
        counts = [record['value'] for record in month_val]
        month = [counts, names]
        print("names", names)
        print("counts", counts)
        return month

    @api.model
    def  leads_lost_by_month(self):

        company_id = self.env.company

        leads_lost_by_month = len(self.search([('company_id', '=', company_id.id),
                                      ('user_id', '=', self.env.user.id),
                                      ('stage_id.name', '=', 'Lost')],order='create_date'))

        plans_data = self._read_group(
            domain=[('company_id', '=', company_id.id),  ('user_id', '=', self.env.user.id),('stage_id.name', '=', 'Lost') ],
            groupby=['create_date'],
            aggregates=['__count'],
        )


        print("plans_data", plans_data)
        print("leads_lost_by_month", leads_lost_by_month)
        # plans_count = {department.id: count for department, count in plans_data}
        # for department in self:
        #     department.plans_count = plans_count.get(department.id,
        #                                              0) + plans_count.get(False,
        #                                                                   0)




