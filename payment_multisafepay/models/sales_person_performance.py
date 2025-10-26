from datetime import date

from odoo import api, fields, models


class SalesPersonPerformance(models.Model):

    _name = 'sale.person.performance'
    _description = 'Sales Person Performance'

    user_id = fields.Many2one('res.partner', string='User')
    month = fields.Datetime(string='Month')
    total_sales_amount = fields.Float(string='Total Sales')
    total_orders = fields.Float(string='Total Orders')
    sales_id = fields.Many2one('sale.order', string='Sales Order')
    



class SaleOrder(models.Model):

    _inherit = 'sale.order'
    his_performance = fields.Integer(string='His Performance Count', default=0)
    performace_ids = fields.One2many('sale.person.performance', 'sales_id', string='Performance Orders')


    def go_to_his_performance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Person Performance',
            'res_model': 'sale.person.performance',
            'view_mode': 'form,list',
            'target': 'current',
            'res_id':hsp.id

        }
    def action_confirm(self):

        # print(len(self.performace_ids.search([('user_id','=', self.user_id.id)])))
        self.write({'his_performance':len(self.performace_ids.search([('user_id','=', self.user_id.id)]))
        })

        today = date.today()

        total_his_sales = self.search([('user_id','=',self.user_id.id)])
        total_his_sales_amount = sum(total_his_sales.mapped('amount_total'))
        print("total_his_sales",total_his_sales)
        print("total_his_sales_amount", total_his_sales_amount)
        global hsp
        hsp = self.env['sale.person.performance'].create({
            'user_id': self.user_id.id,
            'month': today,
            'total_sales_amount': total_his_sales_amount,
            'total_orders': len(total_his_sales),

        })



        return super(SaleOrder, self).action_confirm()


