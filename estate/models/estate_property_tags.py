from odoo import models, fields


class EstateTags(models.Model):
    _name = "property.tags"
    _description = "property tags description"
    _order = "name asc"

    name = fields.Char("Property Tags", required=True)
    color= fields.Integer()

    _sql_constraints = [
        ('UniqueTag', 'UNIQUE(name)',
         'Tag Must be Unique!')
    ]
