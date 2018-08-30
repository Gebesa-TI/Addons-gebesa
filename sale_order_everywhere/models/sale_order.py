# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # group_obj = self.env['procurement.group']
        # move_obj = self.env['stock.move']
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            # group = group_obj.search([('sale_id', '=', order.id)])
            # for procurement in group.procurement_ids:
            #     procurement.sale_id = group.sale_id
            #     if procurement.production_id:
            #         procurement.production_id.sale_id = group.sale_id
            # moves = move_obj.search([('group_id', '=', group.id)])
            # for move in moves:
            #     move.sale_id = group.sale_id

            self._cr.execute('UPDATE procurement_order po SET sale_id = %s '
                             'FROM procurement_group pg WHERE pg.sale_id = %s '
                             'AND pg.id = po.group_id', (order.id, order.id,))
            if not order.dealer_id:
                dealer= None
            else:
                dealer = order.dealer_id.id
            self._cr.execute('UPDATE mrp_production mp SET sale_id = %s, '
                             'partner_id = %s, client_order_ref = %s, '
                             'warehouse_id = %s, city_shipping = %s, '
                             'dealer_id = %s '
                             'FROM procurement_group pg '
                             'join procurement_order po on pg.id = po.group_id '
                             'WHERE pg.sale_id = %s AND po.production_id = mp.id',
                             (order.id, order.partner_id.id, order.client_order_ref,
                              order.warehouse_id.id, order.partner_shipping_id.city,
                              dealer,order.id,))
            self._cr.execute('UPDATE stock_move sm SET sale_id = %s '
                             'FROM procurement_group pg '
                             'WHERE pg.sale_id = %s AND pg.id = sm.group_id',
                             (order.id, order.id,))
            self._cr.execute('UPDATE stock_picking sp SET sale_id = %s '
                             'FROM procurement_group pg '
                             'join stock_move sm on pg.id = sm.group_id '
                             'WHERE pg.sale_id = %s AND sm.picking_id = sp.id',
                             (order.id, order.id,))
        return res
