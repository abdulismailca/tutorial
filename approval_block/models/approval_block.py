from odoo import api, fields, models


class ApprovalBlock(models.Model):

    _name = 'approval.block'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description= 'Approval Block'

    name = fields.Char(string="Name", required=True, tracking=True)
    limit_amount = fields.Integer(string="Limit Amt",required=True, tracking=True)

    po_reference_ids = fields.One2many('purchase.order','approval_block_id', string="PO Reference", compute="compute_po_reference_ids")


    def compute_po_reference_ids(self):

        po_with_limit = self.env['purchase.order'].search([('amount_total','<=',self.limit_amount)])

        print('po_with_limit', po_with_limit)


        self.update({
            'po_reference_ids':[(fields.Command.link(po.id)) for po in po_with_limit]
        })

