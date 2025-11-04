from odoo import fields,models


class CrmTeam(models.Model):

    _inherit = 'crm.team'

    stage_id = fields.Many2one('crm.stage',"Lead Stage")