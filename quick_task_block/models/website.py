# Part of Odoo. See LICENSE file for full copyright and licensing details.
from email.policy import default

from odoo import SUPERUSER_ID, api, fields, models, tools
from odoo.http import request
from odoo.osv import expression
from odoo.tools.translate import _, LazyTranslate


# class Website(models.Model):
#     _inherit = 'website'


class SaleOrder(models.Model):


    _inherit ='sale.order'

    wh_count = fields.Integer("wh stock", default=7)







