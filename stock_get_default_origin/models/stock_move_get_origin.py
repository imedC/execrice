from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit='stock.picking'

    client_note = fields.Char(compute='compute_client_note_',inverse='inverse_client_note', store=True)

    @api.one
    @api.depends('sale_id.client_note')
    def compute_client_note_(self):

        client_note = self.env["sale.order"].search([("id", "=", self.sale_id.id)]).client_note
        self.client_note = client_note

    def inverse_client_note(self):
        return True



class StockMove(models.Model):
    _inherit = 'stock.move'

    client_note = fields.Char(compute='compute_client_note_')

    @api.depends('picking_id.client_note')
    def compute_client_note_(self):

        client_note = self.env["stock.picking"].search([("id", "=", self.picking_id.id)]).client_note
        self.client_note = client_note