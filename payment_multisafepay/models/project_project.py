from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    progress = fields.Float(string="Progress", compute="compute_progress", store=True)

    @api.depends('task_ids.stage_id')
    def compute_progress(self):

        for project in self:

            total = len(project.task_ids)
            # print(project.task_ids.stage_id)
            # for task in project.task_ids.stage_id:
                # print(task.name)
            done = len(project.task_ids.filtered(lambda t: t.stage_id.name == 'Done'))
            # done = len(project.task_ids.filtered(lambda t: t.stage_id.fold))

            """
            actullay the name may change based on user input
            while they creating stage they give differnt name 
            and so we can use the commend line above 'stage_id.fold'
            odoo provide default boolean, but the think is we need 
            to set the stage in fold state.
            
            """

            print(done)
            if done:
                project.progress = (done / total * 100) if total else 0
