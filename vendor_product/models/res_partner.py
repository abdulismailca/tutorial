from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit ='res.partner'

    product_ids = fields.One2many('product.product','product_id', compute="compute_his_product")



    @api.depends()
    def compute_his_product(self):

        all_product_filtered = self.env['product.product'].search([('seller_ids.partner_id', '=', self.id)])

        print("all_product_filtered", all_product_filtered)


        self.update({
            'product_ids':[(fields.Command.link(a.id)) for a in all_product_filtered]
        })




