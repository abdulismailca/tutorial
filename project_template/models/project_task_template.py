from odoo import fields, models, Command


class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'
    _description = 'Project Task Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='name')
    project_id = fields.Many2one('project.project',string="Project")
    milestone_id = fields.Many2one('project.milestone', string='Milestone')
    user_ids = fields.Many2many('res.users', string="Assignees")
    tag_ids = fields.Many2many('project.tags', string='Tags')
    partner_id = fields.Many2one('res.partner', string='Customer')
    description = fields.Html(string='Description')
    task_count = fields.Integer(string="Task Count")

    project_template_id = fields.Many2one('project.template',string="Project Template")


    project_task_id = fields.Many2one('project.task')

    parent_id = fields.Many2one('project.task.template')
    task_template_id = fields.One2many('project.task.template','parent_id')



    # child_ids = fields.Many2many('project.task','parent_id')

    """jus for count smart button"""
    related_task_ids = fields.One2many('project.task', 'project_task_template_id', string="Related Task")



    def create_task_from_temp(self):
        user_ids_list = self.mapped('user_ids')
        tag_ids_list = self.mapped('tag_ids')
        # child_id_list = self.mapped('task_template_id')
        child_id_list = [(fields.Command.create({'name':a.name, 'project_id':self.project_id.id})) for a in self.task_template_id]

        created_task = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'milestone_id': self.milestone_id.id,
            'user_ids': user_ids_list,
            'tag_ids': tag_ids_list,
            'partner_id': self.partner_id.id,
            'description': self.description,
            'project_task_template_id':self.id,
            'child_ids':child_id_list,


        })
        self.write({'task_count':len(self.related_task_ids)})

        print("len of task id",  len(self.related_task_ids))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'res_model': 'project.task',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_task.id,
        }




    def view_related_task(self):
        print("len ", len(self.related_task_ids))
        related_task_list =[]
        for id in self.related_task_ids:
            related_task_list.append(id.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Task',
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id', 'in',related_task_list)],

        }