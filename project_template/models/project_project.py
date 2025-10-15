from odoo import fields, models, Command, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    project_template_id = fields.Many2one("project.template", string="Project template", readonly=True)
    project_project_template_count = fields.Integer(string="Template Count", compute="count_of_project_project")
    serial_number = fields.Integer(string="Serial Number", default="0001")
    project_template_ids = fields.One2many("project.template", "project_id", string="Project Templates")


    def count_of_project_project(self):
        self.write({'project_project_template_count':len(self.project_template_ids)})
        print("from project project", self.project_template_ids )

    def create_project_template(self):
        tag_ids_list = self.mapped('tag_ids')

        task_ids_list = self.mapped('task_ids')

        print("task ids list",task_ids_list)
        print("tag_ids_list ids list",tag_ids_list)

        # for task in self.task_ids:
        #     task_ids_list.append (Command.create({
        #         '
        #     }))

        count = self.serial_number
        count_str =str(count)


        created_template_id = self.env['project.template'].create({
            'name':self.name+" - P"+count_str,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,
            'task_ids':task_ids_list,
            'company_id':self.company_id.id,
         })
        self.serial_number = self.serial_number + 1



        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Templates',
            'res_model': 'project.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_template_id.id,
        }

    def see_project_template(self):
        # ivide lmit koduth avasanathe eduthoode, template count vech
        related_project_list = self.project_template_ids.search([])
        for id in self.project_template_ids:
            related_project_list.append(id.id)

        print("related_project_list",related_project_list)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Project',
            'res_model': 'project.project',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id', 'in', [related_project_list])],
        }





