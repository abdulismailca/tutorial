from odoo import fields, models


class MachineTypes(models.Model):
    _name = 'machine.types'
    _description = 'machine types'


    name = fields.Char("Machine Types", required=True)











