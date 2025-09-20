from datetime import timedelta
from odoo import api, exceptions
from odoo import models, fields
from odoo.fields import Datetime
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "property.name"
    _description = "property description"

    #here we are ordering id
    _order = "id desc"

    name = fields.Char("Name", required=True)
    description = fields.Text()
    postcode = fields.Char("postcode")
    date_availability = fields.Date("Available Form", default=Datetime.now() + timedelta(90), copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(defult=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Area")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')

    ])
    active = fields.Boolean(default=True)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    stage = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Cancelled')
        ],
        string="State",
        required=True,
        copy=False,
        default='new'
    )

    property_types = fields.Many2one("property.types", string="Property Type")

    property_tags = fields.Many2many("property.tags", string="Property Tags")

    sales_man = fields.Many2one("res.users", string="Sales Man")

    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)

    offer = fields.One2many("property.offer", "property_id", string="Offer")

    total_area = fields.Float(compute="compute_total")

    best_price = fields.Float(compute="compute_best_price")

    # status_stage = fields.Selection([('new', 'New'), ('canceled', 'Canceled'), ('sold', 'Sold')], default='new',
    #                                 required=True, string="Stage")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price>0)',
         'Expected Price Must be Positive!')
    ]
    _sql_constraints = [
        ('selling_price', 'CHECK(selling_price>0)',
         'Selling Price Must be Positive!')
    ]



    # total area calculation

    @api.depends('garden_area', 'living_area')
    def compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best price setting function
    @api.depends('offer')
    def compute_best_price(self):
        for record in self:
            if record.offer:
                record.best_price = max(record.offer.mapped(
                    'price'))  # offer is variable here(actually it is a row in offer property table, that contain a value )
            else:
                record.best_price = 0.0

    # garden area and orientation checking
    @api.onchange("garden")
    def _garden_onchange(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = ''

    # sold and cancel button function


    def action_sold(self):
        if self.stage == "canceled":
            raise exceptions.UserError("Canceled property can't be sold ")
        else:
            self.stage = 'sold'

    def action_cancel(self):
        if self.stage == "sold":
            raise exceptions.UserError("Sold property can't be canceled")
        else:
            self.stage = "canceled"


    @api.constrains(" expected_price","selling_price","best_price")
    def check_value(self):
        for record in self:
            if  record.expected_price <0 or record.selling_price <0 or record.best_price <0:
                raise exceptions.UserError("Value must be positive")

    @api.constrains("selling_price")
    def check_value(self):
        for record in self:
           ex_value= record.expected_price *0.9
           if float_compare(record.selling_price,ex_value,precision_digits=2)==-1:
               raise exceptions.UserError("Value less than 90% expected ")


