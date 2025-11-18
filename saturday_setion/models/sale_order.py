from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_name = fields.Char(string="Partner Name")


    # case 2: fields access cheyoumbo , dependas marumbo youm
    # case 3
    # case 4: no depends but there is store, only first time work, because there is no value in DB

    @api.onchange('partner_id')
    def _onchange_partner_id(self):

        # self.update({'partner_name':'partner_id.name'})
        print("hello")

    def action_confirm(self):

        #search_count : simply we can found record set count
        # all_so = self.search_count([('partner_id','=', self.partner_id.id),('state','=','sale')])

        #search_read: we can give domain, field, to find list of dict
        # all_so = self.search_read([('partner_id','=', self.partner_id.id),('state','=','sale')])

        # read: we can give parameters(fields,), all ready ulla nte key,value  dict ayi kittum
        # all_so = self.read([])

        # browse: we can give parameters(fields,), all ready ulla nte key,value  dict ayi kittum
        # all_so = self.browse(1)

        #filtered :

        # all_so = self.search([])
        #
        # all_so_filtered = all_so.filtered(lambda s: s.partner_id == self.partner_id and s.state == 'sale')


        all_so = self.search([])
        print("all_so", all_so)
        all_mapped_pricelist_id = all_so.mapped('pricelist_id')



        print('all_mapped_pricelist_id', all_mapped_pricelist_id)

        self.write({'partner_name': 'Ismail C A'})
        print( self.partner_name)

