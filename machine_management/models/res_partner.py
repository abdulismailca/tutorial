from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    machine_ids = fields.One2many("machine.management", "customer_id")
    count_of_machine = fields.Integer(string="Number of Machines",
                                      compute='compute_count_of_machines',
                                      store=True)#store = True is use for save in data base , because it computed field , it does not save in db


    def action_archive(self):

        for record in self:
            un_archive_record = record.machine_ids

            #un_archive_record.write({'active':False})

            un_archive_record.action_archive()

        return super(ResPartner, self).action_archive()

    def action_unarchive(self):
        for record in self:
            archive_record = self.machine_ids.search(
                [
                    ('customer_id', '=', record.id),
                    ('active', '=', False)
                ]
            )
            archive_record.write({'active': True})

        return super(ResPartner, self).action_unarchive()

    """ customer related machines"""

    def get_customer_related_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine Management',
            'res_model': 'machine.management',
            'view_mode': 'list,form',
            'domain': [('customer_id', '=', self.id)],

        }


    """  customer related machines count"""

    @api.depends('machine_ids')
    def compute_count_of_machines(self):
        for record in self:
            len_of_machine = len(record.machine_ids)
            record.write({'count_of_machine': len_of_machine})
