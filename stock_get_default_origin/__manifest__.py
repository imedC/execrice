# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock move get origin',
    'version': '10.0',
    'category': 'Stock',
    'sequence': 3,
    'depends': ['base','stock','sale', 'sale_stock'
    ],
    'data': [
    'views/sale_order_add_field.xml',
    'views/stock_picking_add_field.xml',
    'views/stock_move_add_field.xml'
    ],


}
