
from odoo import fields,models

class MachineParts(models.Model):
    _name="machine.parts"
    _description = "machine parts"


    machine_name_id =fields.Many2one("machine.management",string="Machine Management")

    machine_service_parts_id = fields.Many2one("machine.service",string="Machine Service")

    machine_parts_id = fields.Many2one("product.product",string="Products")


    machine_uom_id = fields.Many2one("uom.uom", string="UoM")

    machine_parts_qty = fields.Integer(string="Quantity", default=1)

