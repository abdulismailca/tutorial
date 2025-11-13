import calendar
import datetime

from odoo import models, api, fields


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


    @api.model
    def lead_by_month_table(self, period='monthly'):
        """Return lead count grouped by selected period."""
        leads = self.search([('create_date', '!=', False)])
        now = fields.Datetime.now()

        print("period", period)

        grouped_data = {}

        for rec in leads:
            if period == 'weekly':
                week = rec.create_date.strftime("Week %U (%b)")
                grouped_data[week] = grouped_data.get(week, 0) + 1
            elif period == 'quarterly':
                q = (rec.create_date.month - 1) // 3 + 1
                key = f"Q{q} {rec.create_date.year}"
                grouped_data[key] = grouped_data.get(key, 0) + 1
            elif period == 'yearly':
                year = rec.create_date.year
                grouped_data[year] = grouped_data.get(year, 0) + 1
            else:  # monthly
                month = calendar.month_name[rec.create_date.month]
                grouped_data[month] = grouped_data.get(month, 0) + 1

        names = list(grouped_data.keys())
        counts = list(grouped_data.values())

        print(f"Filter={period}, Data={grouped_data}")
        return [counts, names]

    @api.model
    def get_lost_won_graph_data(self):
        company_id = self.env.company
        user = self.env.user
        domain = [('company_id', '=', company_id.id), ('user_id', '=', user.id)]

        total_won = self.search_count(domain + [('stage_id.name', '=', 'Won')])
        total_lost = self.search_count(
            domain + [('stage_id.name', '=', 'Lost')])
        total_open = self.search_count(
            domain + [('stage_id.name', 'not in', ['Won', 'Lost'])])

        return {
            'labels': ['Won', 'Lost', 'Open'],
            'values': [total_won, total_lost, total_open],
        }

    @api.model
    def lead_by_campaign(self):
        company_id = self.env.company
        user = self.env.user
        leads = self.search([
            ('company_id', '=', company_id.id),
            ('user_id', '=', user.id),
            ('campaign_id', '!=', False)
        ])

        campaigns = leads.mapped('campaign_id.name')
        result = {}
        for c in campaigns:
            result[c] = result.get(c, 0) + 1

        return {
            'labels': list(result.keys()),
            'values': list(result.values()),
        }

    @api.model
    def get_lost_won_graph_data(self):
        company_id = self.env.company
        user = self.env.user
        domain = [('company_id', '=', company_id.id), ('user_id', '=', user.id)]

        total_won = self.search_count(domain + [('stage_id.name', '=', 'Won')])
        total_lost = self.search_count(
            domain + [('stage_id.name', '=', 'Lost')])
        total_open = self.search_count(
            domain + [('stage_id.name', 'not in', ['Won', 'Lost'])])

        return {
            'labels': ['Won', 'Lost', 'Open'],
            'values': [total_won, total_lost, total_open],
        }






