# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )

    @api.multi
    def action_cancel(self):
        result = super(StockMove, self).action_cancel()
        for move in self:
            if move.production_id and move.production_id.segment_line_ids:
                production = move.production_id
                manufacture_qty = 0
                for move_create in production.move_created_ids:
                    manufacture_qty += move_create.product_uom_qty
                production.segment_line_ids.manufacture_qty = manufacture_qty
        return result

    @api.multi
    def action_done(self):
        result = super(StockMove, self).action_done()
        procurement_obj = self.env['procurement.order']
        segments = []
        for move in self:
            if move.production_id and move.production_id.segment_line_ids:
                production = move.production_id
                manufacture_qty = 0
                for move_create in production.move_created_ids:
                    manufacture_qty += move_create.product_uom_qty
                production.segment_line_ids.manufacture_qty = manufacture_qty
                product_qty = production.segment_line_ids.product_qty

                if manufacture_qty == 0:
                    segment = production.segment_line_ids.segment_id
                    if segment not in segments:
                        segments.append(segment)

                procurement = procurement_obj.search([
                    ('production_id', '=', production.id)])
                group = procurement.group_id
                move_dest = procurement.move_dest_id.move_dest_id
                procurement2 = procurement_obj.search([
                    ('group_id', '=', group.id),
                    ('product_id', '=', production.product_id.id),
                    ('sale_line_id', '!=', False),
                    ('move_ids', '=', move_dest.id)])
                if procurement2:
                    procurement2.sale_line_id.write(
                        {'segment_qty': product_qty - manufacture_qty})

        for seg in segments:
            done = True
            for produ in seg.line_ids:
                if produ.manufacture_qty > 0:
                    done = False
                produ.quantity = 0
            if done:
                # seg.write({'state': 'done'})
                self.env.cr.execute(
                    "update mrp_segment set state = 'done' where id = %s",
                    (seg.id,))
        return result
