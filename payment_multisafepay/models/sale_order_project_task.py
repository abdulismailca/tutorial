from datetime import date, datetime

from odoo import fields, models, api, Command
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):

    _inherit = "sale.order"

    project_id = fields.Many2one("project.project", string="Project")
    his_own_project_ids = fields.Many2many("project.project")



    @api.onchange("partner_id")
    def compute_his_project(self):

        print("compute_his_project")


        his_project = self.his_own_project_ids.search([])
        print("project_id",his_project)

        his_filtered_data =his_project.filtered(lambda s: s.partner_id == self.partner_id)
        print("filterd data",his_filtered_data)
        if his_filtered_data:
            self.update({
                'his_own_project_ids': [(fields.Command.link(a.id)) for a in his_filtered_data]
            })
        else:

            self.update({
                'his_own_project_ids': [(fields.Command.clear())]
            })

    def create_task(self):

        child_tasks = []
        task_amount = []
        for line in self.order_line:
            task_amount.append(line.price_unit)
        line_high_amount =max(task_amount)

        for line in self.order_line:

            

            child_tasks.append(Command.create(
                {
                    'name': f'{line.product_template_id.name} -Qty:{line.product_uom_qty}',
                    'user_ids': [self.env.uid],
                    'priority': '1' if line.price_unit == line_high_amount else 0,

                }
            ))

        print(child_tasks)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Task',
            'res_model': 'project.task',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f'SO/{self.display_name}-{self.partner_id.name}',
                'default_project_id': self.project_id.id,
                'default_description':'qwerty',
                'default_user_ids':[self.env.uid],
                'default_child_ids':child_tasks,


            }

        }


    







