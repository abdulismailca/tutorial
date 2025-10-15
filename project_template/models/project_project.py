from odoo import fields, models, Command, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    project_template_id = fields.Many2one("project.template", string="Project template", readonly=True)
    project_project_template_count = fields.Integer(string="Template Count")



    def create_project_template(self):
        tag_ids_list = self.mapped('tag_ids')

        task_ids_list = self.mapped('task_ids')

        print("task ids list",task_ids_list)
        print("tag_ids_list ids list",tag_ids_list)

        # for task in self.task_ids:
        #     task_ids_list.append (Command.create({
        #         '
        #     }))

        created_template_id = self.env['project.template'].create({
            'name':self.name,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,
            'task_ids':task_ids_list,
            'company_id':self.company_id.id,
         })



        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Templates',
            'res_model': 'project.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_template_id.id,
        }

    def see_project_template(self):

        print("project_template_id ssss",self.project_template_id)




