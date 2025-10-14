from odoo import fields, models, Command, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    project_template_id = fields.Many2one("project.template", string="Project template")


    @api.onchange('project_template_id')
    def link_project_template(self):
       tag_id_list = self.mapped('project_template_id.tag_ids')


       self.write({'name':self.project_template_id.name})
       self.write({'label_tasks':self.project_template_id.label_tasks})
       self.write({'user_id': self.project_template_id.user_id})
       self.write({'description': self.project_template_id.description})
       self.write({'tag_ids':tag_id_list})






    def create_project_template(self):
        tag_ids_list = self.mapped('tag_ids')

        print("tag ids",tag_ids_list)

        self.env['project.template'].create({
            'name':self.name,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,

        })

    # label_task = fields.Char(string="Task Label")
    # partner_id = fields.Many2one("res.partner", string="Partner")
    # tag_ids = fields.Many2many("project.tags", string="project Tags")
    # user_id = fields.Many2one("res.users", string="project Manager")
    # description = fields.Html(string="Description")
