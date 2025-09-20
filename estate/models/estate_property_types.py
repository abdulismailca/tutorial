from odoo import models, fields


class EstateTypes(models.Model):
    _name = "property.types"
    _description = "property types description"
    _order = "name asc"

    name = fields.Char("Property Types", required=True)
    types_data = fields.One2many("property.name", "property_types", string="Types", readonly=True)
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('UniqueTypes', 'UNIQUE(name)',
         'Typ Must be Unique!')
    ]
