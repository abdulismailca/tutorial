from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit ='res.partner'

    product_ids = fields.One2many('product.product','product_id', compute="compute_his_product")



    @api.depends()
    def compute_his_product(self):

        all_product = self.env['product.product'].search([])

        product_vendor = all_product.mapped('seller_ids')

        all_product_filtered = all_product.filtered(lambda s: self in s.seller_ids.partner_id)
        # all_product_filtered = all_product.filtered(lambda s: self.id in s.seller_ids.partner_id)


        print("seller_ids",product_vendor)
        print("all_product_filtered", all_product_filtered)


        self.update({
            'product_ids':[(fields.Command.link(a.id)) for a in all_product_filtered]
        })




