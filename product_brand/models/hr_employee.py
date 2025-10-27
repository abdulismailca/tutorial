from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    partner_id = fields.Many2one('res.partner')
    count_of_po = fields.Integer()
    count_of_so = fields.Integer()


    def view_count_of_po(self):
        # all_so = self.env['sale.order'].search([()])
        # all_so.action_confirm()
        pass


    def view_count_of_so(self):
        pass

    # @api.depends(lambda self: self._get_partner_count_depends())
    # def _compute_related_partners_count(self):
    #     self.related_partners_count = len(self._get_related_partners())
    #
    # def _get_related_partners(self):
    #     return self.work_contact_id | self.user_id.partner_id
    #
    # def action_related_contacts(self):
    #     related_partners = self._get_related_partners()
    #     action = {
    #         'name': _("Related Contacts"),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'res.partner',
    #         'view_mode': 'form',
    #     }
    #     if len(related_partners) > 1:
    #         action['view_mode'] = 'kanban,list,form'
    #         action['domain'] = [('id', 'in', related_partners.ids)]
    #         return action
    #     else:
    #         action['res_id'] = related_partners.id
    #     return action
