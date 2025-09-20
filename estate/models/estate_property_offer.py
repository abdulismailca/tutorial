from datetime import *
from odoo import models, fields, api
from odoo.fields import Datetime


class EstateTags(models.Model):
    _name = "property.offer"
    _description = "property Offer description"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refuse', 'Refuse')], string="Status" )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner ID")
    property_id = fields.Many2one("property.name", required=True, string="Property ID")
    validity_date=fields.Integer(string="Validity",default=7)
    dead_line= fields.Datetime(compute="_deadline_date", inverse="_inverse_date")

    _sql_constraints = [
        ('price', 'CHECK(offer>0)',
         'offer Price Must be Positive!')
    ]



#validity date calculation
    @api.depends("validity_date")
    def _deadline_date(self):
        for record in self:
            if record.create_date:
                record.dead_line = record.create_date+timedelta(days=record.validity_date)
            else:
                record.create_date = Datetime.now()
                record.dead_line = record.create_date+ timedelta(days=record.validity_date)

#validty calculation
    def _inverse_date(self):
        for record in self:
            record.validity_date =(record.dead_line - record.create_date).days


#offer Accept & Refuse / when confirm the offer price and
    def action_confirm(self):
        for record in self:
            record.property_id.selling_price=record.price
            record.property_id.buyer=record.partner_id
            record.status="accepted"
            record. property_id.stage="offer_accepted"

    def action_cancel(self):
        self.status="refuse"


