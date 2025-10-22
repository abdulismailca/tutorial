from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit ='res.partner'

    product_ids = fields.One2many('product.product','product_id', compute="compute_his_product")
    alternative_product_ids = fields.One2many('product.product','product_id')



    @api.depends()
    def compute_his_product(self):

        all_product = self.env['product.product'].search([])

        all_product_filtered = all_product.seller_ids.filtered(
            lambda s: s.partner_id.id == self.id)

        # mapped_product = all_product_filtered.mapped('product_id')
        # print("mapped product", mapped_product)


        for pr in all_product_filtered:
            print("name", pr.product_tmpl_id.id)


        self.update({
            'product_ids':[(fields.Command.link(
                a.product_tmpl_id.id
            )) for a in all_product]
        })

