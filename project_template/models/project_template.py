from odoo import fields, models, Command, api


class ProjectTemplate(models.Model):

    _name = 'project.template'
    _description = 'Project Task Templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Project", tracking=True)
    label_tasks = fields.Char(string="Name of the task", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Partner", tracking=True)
    tag_ids = fields.Many2many("project.tags", string="project Tags", tracking=True)
    user_id = fields.Many2one("res.users",string="project Manager", tracking=True)
    description = fields.Html(string="Description", tracking=True)
    company_id = fields.Many2one("res.company", string="Company", tracking=True)
    task_ids = fields.One2many("project.task",'project_template', string="Tasks", tracking=True, default=None)
    project_count = fields.Integer(string="Project Count")

    related_project = fields.One2many("project.project", "project_template_id", string="Related Project")

    project_task_template_ids = fields.Many2many('project.task.template', 'project_template_id', string="Task Templates")








    def create_project_from_temp(self):

        tag_ids_list = self.mapped('tag_ids')
        task_ids_list = self.mapped('project_task_template_ids.id')
        print("task is undo task undo", task_ids_list)

        # for task in self.task_ids:
        #     task_ids_list.append(Command.create({
        #         'name': task.name,
        #     }))


        created_project =self.env['project.project'].create({
            'name': self.name,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,
            'company_id': self.company_id.id,
            'task_ids': task_ids_list,
            'project_template_id':self.id,

        })
        self.write({'project_count': len(self.related_project)})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Templates',
            'res_model': 'project.project',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_project.id,
        }


    def view_related_project(self):


        print("related project id", self.related_project)
        related_project_list = []
        for id in self.related_project:
            related_project_list.append(id.id)

        print("related project", related_project_list)


        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Project',
            'res_model': 'project.project',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id', 'in', related_project_list)],
        }
