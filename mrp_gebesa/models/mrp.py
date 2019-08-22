# -*- coding: utf-8 -*-
# © <2016> <César Barrón Butista>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    procurement_ids = fields.One2many(
        'procurement.order',
        'production_id',
        string='Procurement',
    )
    trace = fields.Char(
        string='Trace',
        compute='_compute_trace',
        store=True,
    )
    picking_raw_material_ids = fields.Many2many(
        'stock.picking',
        string='Picking Raw Material',
        compute='_compute_picking_raw_material_ids',
    )
    picking_move_prod_id = fields.Many2one(
        'stock.picking',
        string='Picking Production',
        compute='_compute_picking_move_prod_id',
        # store=True,
    )
    cancellation_reason = fields.Text(
        string='Cancellation reason',
    )

    transfer_status = fields.Selection(
        [('not_transferred', _('Not transferred')),
         ('transferred', _('Transferred'))],
        string=_("Transfer status"),
        compute='_compute_transfer_status',
        # store=True,
    )

    state = fields.Selection(
        selection_add=[('transfer', _('Traspasado'))],
    )

    @api.depends('move_prod_id')
    def _compute_picking_move_prod_id(self):
        for prod in self:
            move = prod.move_prod_id
            prod.picking_move_prod_id = move.picking_id.id

    @api.depends('move_lines', 'move_lines2')
    def _compute_picking_raw_material_ids(self):
        move_obj = self.env['stock.move']
        for prod in self:
            moves = []
            for move in prod.move_lines:
                moves.append(move.id)
            for move in prod.move_lines2:
                moves.append(move.id)
            moves_dest = move_obj.search([('move_dest_id', 'in', moves)])
            pickings = []
            for mov in moves_dest:
                if mov.picking_id.id not in pickings:
                    pickings.append(mov.picking_id.id)
            prod.picking_raw_material_ids = pickings

    @api.depends(
        'procurement_ids',
        'procurement_ids.move_dest_id.picking_id',
        'procurement_ids.move_dest_id.move_dest_id.picking_id',
        'procurement_ids.move_dest_id.move_dest_id.move_dest_id.picking_id',
        'procurement_ids.move_dest_id.move_dest_id.move_dest_id.move_dest_id.picking_id')
    def _compute_trace(self):
        return
        # for production in self:
        #     production.trace = ''
        #     produrement = production.procurement_ids
        #     if produrement.move_dest_id:
        #         sm1 = produrement.move_dest_id
        #         if sm1.origin:
        #             production.trace += sm1.origin + ', '
        #         if sm1.picking_id.name:
        #             production.trace += sm1.picking_id.name
        #         if sm1.move_dest_id.picking_id:
        #             sm2 = sm1.move_dest_id
        #             production.trace += ', ' + sm2.picking_id.name
        #             if sm2.move_dest_id.picking_id:
        #                 sm3 = sm2.move_dest_id
        #                 if sm3.picking_id.name:
        #                     production.trace += ', ' + sm3.picking_id.name
        #                 if sm3.move_dest_id.picking_id:
        #                     sm4 = sm3.move_dest_id
        #                     production.trace += ', ' + sm4.picking_id.name

    @api.depends('state', 'move_created_ids2',
                 'move_created_ids2.move_dest_id',
                 'move_created_ids2.move_dest_id.state')
    def _compute_transfer_status(self):
        for prod in self:
            transfer = True
            prod.transfer_status = 'not_transferred'
            if prod.move_created_ids:
                transfer = False
                continue
            for move in prod.move_created_ids2:
                if move.state != 'done':
                    transfer = False
                    continue
                if move.move_dest_id.state != 'done':
                    transfer = False
                    continue
            if transfer:
                prod.transfer_status = 'transferred'
                if prod.state == 'done':
                    self.env.cr.execute("""UPDATE mrp_production SET state = 'transfer'
                                        WHERE id = %s """ % (prod.id))

    def _make_consume_line_from_data(
            self, cr, uid, production, product,
            uom_id, qty, context=None):
        stock_move = self.pool.get('stock.move')
        loc_obj = self.pool.get('stock.location')
        # Internal shipment is created for Stockable and Consumer Products
        if product.type not in ('product', 'consu'):
            return False

        # Take routing location as a Source Location.
        source_location_id = production.location_src_id.id
        bom_id = production.bom_id.id
        if bom_id:
            bomline_obj = self.pool['mrp.bom.line']
            blines = bomline_obj.search(
                cr, uid, [
                    ('bom_id', '=', bom_id),
                    ('product_id', '=', product.id)],
                limit=1, context=context)

            if blines and bomline_obj.browse(
                cr, uid, blines[0],
                    context=context).location_id:
                source_location_id = bomline_obj.browse(
                    cr, uid, blines[0],
                    context=context).location_id.id

        # Verificar si es necesario cambiar tambien prod_location_id
        prod_location_id = source_location_id
        prev_move = False
        if production.bom_id.routing_id and\
                production.bom_id.routing_id.location_id and\
                production.bom_id.routing_id.location_id.id !=\
                source_location_id:
            source_location_id = production.bom_id.routing_id.location_id.id
            prev_move = True

        destination_location_id =\
            production.product_id.property_stock_production.id
        move_id = stock_move.create(cr, uid, {
            'name': production.name,
            'date': production.date_planned,
            'date_expected': production.date_planned,
            'product_id': product.id,
            'product_uom_qty': qty,
            'product_uom': uom_id,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'company_id': production.company_id.id,
            'procure_method': prev_move and 'make_to_stock' or
            self._get_raw_material_procure_method(
                cr, uid, product,
                location_id=source_location_id,
                location_dest_id=destination_location_id,
                context=context),
            # Make_to_stock avoids creating procurement
            'raw_material_production_id': production.id,
            # this saves us a browse in create()
            'price_unit': product.standard_price,
            'origin': production.name,
            'warehouse_id': loc_obj.get_warehouse(
                cr, uid, production.location_src_id, context=context),
            'group_id': production.move_prod_id.group_id.id,
        }, context=context)

        if prev_move:
            prev_move = self._create_previous_move(
                cr, uid, move_id, product, prod_location_id,
                source_location_id, context=context)
            stock_move.action_confirm(cr, uid, [prev_move], context=context)
        return move_id

    @api.multi
    def action_cancel(self):
        for production in self:
            if not self.env.user.has_group(
                    'system_administrator.group_system_administrator_gebesa'):
                raise UserError(_('Only Administrator can cancel'))

            if not production.cancellation_reason:
                raise UserError(_('Specify the reason for cancellation'))

        res = super(MrpProduction, self).action_cancel()

        for production in self:
            for picking in production.picking_raw_material_ids:
                if picking.state not in ['done', 'cancel']:
                    picking.do_unreserve()
                    moves = ''
                    cancel_pick = True
                    for move in picking.move_lines:
                        if move.state not in ('done'):
                            moves += str(move.id) + ','
                        else:
                            cancel_pick = False
                    if moves != '':
                        moves = moves[:-1]
                        self.env.cr.execute("""
                            UPDATE stock_move SET state = 'cancel'
                            WHERE id in (%s) """ % (moves))
                if cancel_pick:
                    self.env.cr.execute("""
                        UPDATE stock_picking SET state = 'cancel'
                        WHERE id in (%s) """ % (picking.id))

        return res
