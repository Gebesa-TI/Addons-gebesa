# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    acc_move_id = fields.Many2one(
        'account.move',
        string=_(u'Account Move'),
        copy=False
    )

    def action_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()

        # move_obj = self.pool.get('account.move')
        picking_obj = self.pool.get('stock.picking')
        production_obj = self.pool.get('mrp.production')

        res = super(StockMove, self).action_done(cr, uid, ids, context=ctx)

        move_ids = []
        picking_id = False
        production_id = False
        for move in self.browse(cr, uid, ids, context=context):
            if move.acc_move_id:
                move_ids.append(move.acc_move_id.id)
            picking_id = move.picking_id
            production_id = move.production_id or move.raw_material_production_id

        if picking_id:
            picking = picking_obj.browse(cr, uid, picking_id.id, context=ctx)
            picking.am_ids = False
            if move_ids:
                picking.am_ids = move_ids

        if production_id:
            production = production_obj.browse(cr, uid, production_id.id, context=ctx)
            # production.am_ids = False
            if move_ids:
                for move in move_ids:
                    production.write({'am_ids': [(4, move)]})
                # production.am_ids = move_ids or False

        return res
