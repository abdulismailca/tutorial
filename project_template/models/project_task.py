from odoo import fields, models
from odoo.api import readonly


class ProjectTask(models.Model):
    _inherit = 'project.task'

    """ee field vech ann 'project.project' nne task template ekk write cheyounne"""
    project_template = fields.Many2one('project.template', string="Project Task Template")

    project_task_template_id = fields.Many2one('project.task.template',string="Task Template", readonly=True)

    def create_task_template(self):

        user_ids_list = self.mapped('user_ids')
        tag_ids_list = self.mapped('tag_ids')


        created_task_id =self.env['project.task.template'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'milestone_id': self.milestone_id.id,
            'user_ids': user_ids_list,
            'tag_ids': tag_ids_list,
            'partner_id': self.partner_id.id,
            'description': self.description,

        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task Templates',
            'res_model': 'project.task.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_task_id.id,
        }

