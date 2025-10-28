from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    count_of_po = fields.Integer(compute='compute_so_po_count')
    count_of_so = fields.Integer()


    def compute_so_po_count(self):

        self.write({'count_of_po':self.work_contact_id.purchase_order_count})
        self.write({'count_of_so':self.work_contact_id.sale_order_count})

    def view_count_of_po(self):

        contact_po = self.work_contact_id.child_ids+self.work_contact_id
        conatct_po_orders = self.env['purchase.order'].search([('partner_id','in',contact_po.ids)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'view_mode': 'list',
            'target': 'current',
            'domain': [('id', 'in', conatct_po_orders.ids)],
        }

    def view_count_of_so(self):
        contact_so = self.work_contact_id.child_ids.sale_order_ids+self.work_contact_id.sale_order_ids
        print("contact_so", contact_so)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'list',
            'target': 'current',
            'domain': [('id', 'in', contact_so.ids)],
        }

