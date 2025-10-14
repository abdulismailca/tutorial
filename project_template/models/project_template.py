from odoo import fields,models


class ProjectTemplate(models.Model):

    _name = 'project.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Project", tracking=True)
    label_tasks = fields.Char(string="Name of the task", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Partner", tracking=True)
    tag_ids = fields.Many2many("project.tags", string="project Tags", tracking=True)
    user_id = fields.Many2one("res.users",string="project Manager", tracking=True)
    description = fields.Html(string="Description", tracking=True)