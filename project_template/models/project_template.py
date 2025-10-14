from odoo import fields, models, Command


class ProjectTemplate(models.Model):

    _name = 'project.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Project", tracking=True)
    label_tasks = fields.Char(string="Name of the task", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Partner", tracking=True)
    tag_ids = fields.Many2many("project.tags", string="project Tags", tracking=True)
    user_id = fields.Many2one("res.users",string="project Manager", tracking=True)
    description = fields.Html(string="Description", tracking=True)
    company_id = fields.Many2one("res.company", string="Company", tracking=True)
    task_ids = fields.One2many("project.task",'project_id', string="Tasks", tracking=True, default=None)

    def create_project_from_temp(self):

        tag_ids_list = self.mapped('tag_ids')
        task_ids_list = []

        for task in self.task_ids:
            task_ids_list.append(Command.create({
                'name': task.name,
            }))

        print("its task ids from temp", self.task_ids)

        self.env['project.project'].create({
            'name': self.name,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,
            'company_id': self.company_id.id,
            'task_ids': task_ids_list,

        })

