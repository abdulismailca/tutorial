from odoo import models, api

class CrmLead(models.Model):
   _inherit = 'crm.lead'
   @api.model

   def get_tiles_data(self):

       user_all_invoices = self.env['account.move'].search([('invoice_user_id','=',self.user_id.id),('state','=','posted')])
       user_all_invoices_amount = sum(user_all_invoices.mapped('amount_total_in_currency_signed'))

       company_id = self.env.company
       leads = self.search([('company_id', '=', company_id.id),
                            ('user_id', '=', self.env.user.id)])
       my_leads = leads.filtered(lambda r: r.type == 'lead')
       my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
       currency = company_id.currency_id.symbol
       expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
       my_lose = expected_revenue - user_all_invoices_amount


       return {
           'total_leads': len(my_leads),
           'total_opportunity': len(my_opportunity),
           'expected_revenue': expected_revenue,
           'currency': currency,
           'user_all_invoices_amount':user_all_invoices_amount,
           'my_lose':my_lose,
       }
