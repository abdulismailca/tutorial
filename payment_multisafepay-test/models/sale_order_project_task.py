from datetime import date, datetime

from odoo import fields, models, api, Command


class SaleOrder(models.Model):

    _inherit = "sale.order"

    project_id = fields.Many2one("project.project", string="Project")
    his_own_project_ids = fields.Many2many("project.project")
    his_related_task_count = fields.Integer(string="His Related Task Count", compute="count_of_task")
    visible_task_button = fields.Boolean()



    @api.onchange("partner_id")
    def compute_his_project(self):

        print("compute_his_project")


        his_project = self.his_own_project_ids.search([])
        print("project_id",his_project)

        his_filtered_data =his_project.filtered(lambda s: s.partner_id == self.partner_id)
        print("filterd data",his_filtered_data)
        if his_filtered_data:
            self.update({
                'his_own_project_ids': [(fields.Command.clear())]
            })
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
                    'project_id': self.project_id.id,
                    'priority': '1' if line.price_unit == line_high_amount else 0,

                }
            ))

        print(child_tasks)

        self.env['project.task'].create({
            'name': f'SO/{self.display_name}-{self.partner_id.name}',
            'project_id': self.project_id.id,
            'description':'qwerty',
            'user_ids':[self.env.uid],
            'child_ids': child_tasks,


        })



    def sale_order_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Task',
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('partner_id', '=', self.partner_id.id)],


        }

    @api.depends('his_related_task_count')
    def count_of_task(self):
        count_of_task_ids = len(self.partner_id.task_ids)
        print("helo ismial", count_of_task_ids)
        self.his_related_task_count = count_of_task_ids




    







