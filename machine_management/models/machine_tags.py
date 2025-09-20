from odoo import fields, models


class MachineTags(models.Model):
    _name = 'machine.tags'
    _description = 'machine tags'
    _rec_name = 'machine_tags'

    machine_tags = fields.Char(string="Machine Tags")
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('UniqueTag', 'UNIQUE(machine_tags)',
         'Tag Must be Unique!')
    ]












