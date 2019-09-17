
from odoo import api,fields,  models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    check_group = fields.Boolean(compute='check_group_')

    def check_group_(self):

        if self.env['res.users'].has_group('sale_button_visibility.group_cancel_order') or self.state == "draft":
            self.check_group = True
        else:
            self.check_group = False

    def action_cancel(self):
        self.write({'state': 'cancel'})