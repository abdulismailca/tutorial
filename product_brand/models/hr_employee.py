from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    partner_id = fields.Many2one('res.partner')
    count_of_po = fields.Integer()
    count_of_so = fields.Integer()


    def view_count_of_po(self):
        contact_po_mapped = self.work_contact_id.mapped('child_ids')
        conatct_po_orders = self.env['purchase.order'].search([('partner_id','in',contact_po_mapped.ids)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'view_mode': 'list',
            'target': 'current',
            'domain': [('id', 'in', conatct_po_orders.ids)],
        }




    def view_count_of_so(self):
        contact_so_mapped = self.work_contact_id.child_ids.mapped('sale_order_ids')
        print(contact_so_mapped)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'list',
            'target': 'current',
            'domain': [('id', 'in', contact_so_mapped.ids)],
        }

