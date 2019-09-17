# -*- coding: utf-8 -*-
from odoo import api,fields, models, _
from odoo.exceptions import UserError


class account_payment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def create(self, vals):
        res = super(account_payment, self).create(vals)
        print('/*************************************/',vals)
        client_payment = self.env['account.payment'].search([('partner_id','=',vals['partner_id']),('state','=','draft')])
        if len(client_payment) != 1:
            raise UserError(_("Ce client a un paiement à l\'état brouillon, vous devez le confirmer avant d\'en créer un nouveau."))
        return res

