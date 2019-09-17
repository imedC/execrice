# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from collections import Counter
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit='stock.picking'

    @api.model
    def action_merge_delivery(self):
        active_ids = self.env.context['active_ids']
        stock_pickings = self.env['stock.picking']
        move_lines = self.env['stock.move']
        pack_operation_product_ids = self.env['stock.pack.operation']
        p_s_dict = {}
        for sp in stock_pickings.browse(active_ids):
            # sp.write({'state': 'assigned'})

            p_s_dict[str(sp.id)] = str(str(sp.partner_id.id)+ '_'+ sp.state+'_'+str(sp.location_id.id)+'_'+str(sp.location_dest_id.id))

        counts = Counter(p_s_dict.values())
        print('/***COUNT***/', counts)
        for k,v in counts.items():
            if v == 1:
                for k1,v1 in p_s_dict.items():
                    if k == v1:
                        p_s_dict.pop(k1)
        print('/***p_s***/',p_s_dict)
        newDict = {}
        if p_s_dict:
            for k,v in p_s_dict.items():

                for ml in stock_pickings.browse(int(k)).move_lines.ids:
                    if v not in newDict.keys():
                        newDict[v] = [ml]
                    else:
                        newDict[v].append(ml)

                for pack_op in stock_pickings.browse(int(k)).pack_operation_product_ids.ids:
                        if v not in newDict.keys():
                            newDict[v] = [str(pack_op)]
                        else:
                            newDict[v].append(str(pack_op))


            print('/***NEW DICT**/', newDict)
        else:
            raise UserError(_("there is no deliveries to merge"))


        i = 1
        for k,v in newDict.items():

            move_line_dict = {}
            for move_id in v:
                if type(move_id) == int:
                    m_id = move_lines.browse(move_id)
                    if str(m_id.product_id.id)+'_'+str(m_id.location_id.id)+'_'+str(m_id.location_dest_id.id) not in move_line_dict.keys():
                        move_line_dict[str(m_id.product_id.id)+'_'+str(m_id.location_id.id)+'_'+str(m_id.location_dest_id.id)] = m_id.product_uom_qty
                    else:
                        move_line_dict[str(m_id.product_id.id)+'_'+str(m_id.location_id.id)+'_'+str(m_id.location_dest_id.id)] = move_line_dict[str(m_id.product_id.id)+'_'+str(m_id.location_id.id)+'_'+str(m_id.location_dest_id.id)] + m_id.product_uom_qty
            print('/******move_line_dict*****/', move_line_dict)


            pack_op_pro_dict = {}
            for pack_op_id in v:
                if type(pack_op_id) == str:
                    pack_id = pack_operation_product_ids.browse(int(pack_op_id))
                    if str(pack_id.product_id.id)+'_'+str(pack_id.location_id.id)+'_'+str(pack_id.location_dest_id.id) not in pack_op_pro_dict.keys():
                        pack_op_pro_dict[str(pack_id.product_id.id)+'_'+str(pack_id.location_id.id)+'_'+str(pack_id.location_dest_id.id)] = [(pack_id.qty_done, pack_id.product_qty)]
                    else:
                        pack_op_pro_dict[str(pack_id.product_id.id)+'_'+str(pack_id.location_id.id)+'_'+str(pack_id.location_dest_id.id)] = pack_op_pro_dict[str(pack_id.product_id.id)+'_'+str(pack_id.location_id.id)+'_'+str(pack_id.location_dest_id.id)] + [(pack_id.qty_done, pack_id.product_qty)]
            print('/******pack_op_pro_dict*****/', pack_op_pro_dict)


            result_mo_lines = []
            location_dict = {}
            for x, y in move_line_dict.items():
                result_mo_lines.append((0, 0,
                                    {'name': 'ML',
                                   'product_id': int(x.split('_')[0]),
                                   'product_uom': 1,
                                   'product_uom_qty': float(y),
                                   'location_id': int(x.split('_')[1]),
                                   'location_dest_id': int(x.split('_')[2]),
                                   'procure_method': 'make_to_stock'}))

                location_dict['location_id'] = int(x.split('_')[1])
                location_dict['location_dest_id'] = int(x.split('_')[2])

            stock_pickings.create({
                'name': 'wh/merge/'+str(i),
                'partner_id':k.split('_')[0],
                'move_type':'direct',
                'picking_type_id':1,
                'priority':'1',
                'location_id':k.split('_')[2],
                'location_dest_id':k.split('_')[3],
                'move_lines':  result_mo_lines,
            })


            stock_pickings.search([], order='id desc')[0].action_confirm()

            result_pack_op = []
            qty_dict = {}
            for key,val in pack_op_pro_dict.items():

                qty_done = 0
                product_qty = 0
                for x in val:
                    qty_done+=x[0]
                    product_qty+=x[1]
                    qty_dict[key.split('_')[0]] = qty_done
                result_pack_op.append((0, 0,
                            {
                           'picking_id': stock_pickings.search([], order='id desc')[0].id ,
                           'product_id': int(key.split('_')[0]),
                           'location_id': int(key.split('_')[1]),
                           'location_dest_id': int(key.split('_')[2]),
                           'qty_done': qty_done,
                           'product_qty':product_qty}
                ))



            print('/****result_pack_op****/', result_pack_op)
            print('/****qty_d****/',qty_dict)
            stock_pickings.search([], order='id desc')[0].action_assign()
            print(stock_pickings.search([], order='id desc')[0].pack_operation_product_ids)
            for item in stock_pickings.search([], order='id desc')[0].pack_operation_product_ids:
                item.update({
                'qty_done': qty_dict[str(item.product_id.id)]
            })



            for k,v in p_s_dict.items():
                stock_pickings.browse(int(k)).write({'state':'cancel'})

            i+=1