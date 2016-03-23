# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sale Order'),
        ('closed', 'Closed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'), ], string=_(u'Status'), readonly=True,
        copy=False, index=True, track_visibility='onchange', default='draft')

    @api.multi
    def action_closed(self):
        for order in self:
            for pick in order.picking_ids:
                if pick.state in ['draft', 'assigned', 'confirmed']:
                    for rec in pick:
                        moves = [move.id for move in rec.move_lines]
                        self.pool.get('stock.move').action_cancel(
                            self._cr, self._uid, moves, self._context)

        self.write({'state': 'closed'})
        return True


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sale Order'),
        ('closed', 'Closed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], related='order_id.state', string=_(u'Order Status'),
        readonly=True, copy=False, store=True, default='draft')
