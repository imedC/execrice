from odoo import api,fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_note = fields.Char('Client note')
