# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class ResUser(models.Model):
    _inherit='res.users'

    user_connected = fields.Char(default=lambda self: self.env.user.name)
    own_email = fields.Char(default=lambda self: self.env.user.login)

    @api.model
    def action_open_current_user(self):


        view = self.env.ref('base.view_users_form')
        print(self.env.context,self.env.user)
        result = {
            'name': _('Current User'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.users',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.env.user.id,
        }
        return result