from odoo import api, fields, models


class ResUsers(models.Model):
    """Add sessions and buttons in the usr form"""
    _inherit = 'res.users'

    buttons_pos_ids = fields.Many2many('pos.buttons',
                                       string="Pos Buttons",
                                       help="pos buttons")

    def pos_button_visibility(self, hidebuttons):
        """This is used to return the restricted button name"""
        pos_buttons = self.env['pos.buttons'].browse(hidebuttons).mapped('name')
        return pos_buttons

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Loading Fields"""
        result = super()._load_pos_data_fields(config_id)
        result += ['buttons_pos_ids']
        return result

