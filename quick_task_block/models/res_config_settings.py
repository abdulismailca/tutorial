from odoo import fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'


    wh_stock_id = fields.Many2one('stock.location',string="Wh Stock", config_parameter="quick_task_block.wh_stock_id")

