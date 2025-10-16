from odoo import fields, models
from odoo.api import readonly


class ProjectTask(models.Model):
    _inherit = 'project.task'

    """ee field vech ann 'project.project' nne task template ekk write cheyounne"""
    project_template = fields.Many2one('project.template', string="Project Task Template")

    project_task_template_id = fields.Many2one('project.task.template',string="Task Template", readonly=True)

    related_task_template_count = fields.Integer(string="Task template Count" , compute="count_of_task_templates")

    project_task_ids = fields.One2many('project.task.template', 'project_task_id')

    child_id = fields.Many2one('project.template.task')


    def count_of_task_templates(self):

        self.related_task_template_count = len(self.project_task_ids)

    def view_related_task_template(self):


        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Task',
            'res_model': 'project.task.template',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':([('project_task_id','=',self.id)])


        }

    def create_task_template(self):

        user_ids_list = self.mapped('user_ids')
        tag_ids_list = self.mapped('tag_ids')
        # child_task_ids_list = self.mapped('child_ids')

        child_task_ids_list = [(fields.Command.create({'name':a.name, 'project_id':self.project_id.id})) for a in self.child_ids]

        print("child ids -",child_task_ids_list)



        created_task_id =self.env['project.task.template'].create({
            'name': f'TS/{self.id}/{self.name}/{self.partner_id.name if self.partner_id.name else ''}',
            'project_id': self.project_id.id,
            'milestone_id': self.milestone_id.id,
            'user_ids': user_ids_list,
            'tag_ids': tag_ids_list,
            'partner_id': self.partner_id.id,
            'description': self.description,
            'project_task_id': self.id,

            'task_template_id':child_task_ids_list,

        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task Templates',
            'res_model': 'project.task.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_task_id.id,
        }

