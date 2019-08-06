# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    type_adjustment_id = fields.Many2one('type.adjustment',
                                         string=_('Type Adjustment'),
                                         store=True,)
    total_cost = fields.Float(
        string='Totals Cost',
        compute="compute_total_cost"
    )

    @api.depends('move_lines', 'move_lines.product_id',
                 'move_lines.product_uom_qty', 'move_lines.state')
    def compute_total_cost(self):
        for picking in self:
            picking.total_cost = 0.0
            for move in picking.move_lines:
                # import ipdb; ipdb.set_trace()
                if move.state != 'cancel':
                    picking.total_cost += (
                        move.product_uom_qty *
                        move.product_id.standard_price)

    @api.model
    def create(self, vals):
        ctx = self.env.context.copy()
        if 'default_stock_move_type_id' in ctx.keys():
            move_type = self.env['stock.move.type'].browse(
                [ctx['default_stock_move_type_id']])
            if move_type:
                if move_type.code in ('E4', 'S4'):
                    warehouse = self.env.user.employee_ids.default_warehouse_id
                    if move_type.code == 'E4':
                        default = warehouse.in_type_id.id
                    else:
                        default = warehouse.out_type_id.id
                    ctx.update({'default_picking_type_id': default})
        res = super(StockPicking, self.with_context(ctx)).create(vals)
        return res

    @api.multi
    def dynamic_action_adjustment_output(self):
        inventory_lost = self.env['stock.location'].search(
            [('usage', '=', 'inventory')], limit=1)
        ctx = self._context.copy()
        ctx['default_stock_move_type_id'] = 8
        ctx['default_location_dest_id'] = inventory_lost.id
        action = {
            'type': "ir.actions.act_window",
            'name': _('Adjustment OutPut'),
            'res_model': "stock.picking",
            'view_type': "form",
            'view_mode': "tree,form",
            'domain': "[('stock_move_type_id.code', 'in', ['S4']), \
                        ('picking_type_id.code', '=', 'outgoing'), \
                        ('picking_type_id.warehouse_id', '!=', False)]",
            'context': ctx,
        }
        return action

    @api.multi
    def dynamic_action_adjustment_input(self):
        inventory_lost = self.env['stock.location'].search(
            [('usage', '=', 'inventory')], limit=1)
        ctx = self._context.copy()
        ctx['default_stock_move_type_id'] = 7
        ctx['default_location_id'] = inventory_lost.id
        action = {
            'type': "ir.actions.act_window",
            'name': _('Adjustment Input'),
            'res_model': "stock.picking",
            'view_type': "form",
            'view_mode': "tree,form",
            'domain': "[('stock_move_type_id.code', 'in', ['E4']), \
                        ('picking_type_id.code', '=', 'incoming'), \
                        ('picking_type_id.warehouse_id', '!=', False)]",
            'context': ctx
        }
        return action
