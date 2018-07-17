# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sale Order'),
        ('closed', 'Closed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'), ],
        string=_('Status'),
        readonly=True,
        copy=False,
        index=True,
        track_visibility='onchange',
        default='draft')

    closing_reason = fields.Char(
        string=_('Closing Reason'),
    )

    cancel_mo = fields.Boolean(
        string=_('Cancel MO'),
        default=False,
        copy=False,
    )

    @api.multi
    def all_cancel(self):
        # move_obj = self.env['stock.move']
        prod_obj = self.env['mrp.production']
        proc_obj = self.env['procurement.order']
        # purchase_obj = self.env['purchase.order']
        for order in self:
            for pick in order.picking_ids:
                if pick.state in ['draft', 'waiting', 'confirmed',
                                  'partially_available', 'assigned']:
                    pick.do_unreserve()
                    moves = ''
                    cancel_pick = True
                    for move in pick.move_lines:
                        if move.state not in ('done'):
                            moves += str(move.id) + ','
                        else:
                            cancel_pick = False
                    if moves != '':
                        moves = moves[:-1]
                        self.env.cr.execute("""UPDATE stock_move SET state = 'cancel'
                                        WHERE id in (%s) """ % (moves))
                if cancel_pick:
                    self.env.cr.execute("""UPDATE stock_picking SET state = 'cancel'
                                    WHERE id in (%s) """ % (pick.id))
                    # move_obj.browse(moves).action_cancel()
            production = prod_obj.search([('sale_id', '=', order.id)])
            for prod in production:
                if prod.state in ['draft', 'confirmed', 'ready']:
                    self.env.cr.execute("""UPDATE mrp_production SET state = 'cancel'
                                    WHERE id = %s """ % (prod.id))
                    # prod.action_cancel()
            procurement = proc_obj.search([('sale_id', '=', order.id)])
            for proc in procurement:
                if proc.state in ['confirmed', 'exception', 'running']:
                    self.env.cr.execute("""UPDATE procurement_order SET state = 'cancel'
                                    WHERE id = %s """ % (proc.id))
                    # proc.cancel()
            # purchase = purchase_obj.search([('origin', 'like', order.name)])
            # for purc in purchase:
            #    if purc.state in ['draft']:
            #        purc.button_cancel()

    @api.multi
    def action_closed(self):
        for order in self:
            if order.closing_reason is False:
                raise UserError(_("You can't close this Order if you don't"
                                  " captured the Closing Reason field!"))
            if order.invoice_status == 'invoiced':
                raise UserError(_("You can't close this Order if you already"
                                  " in Billed Status!"))
            if order.cancel_mo is True:
                self.all_cancel()
        self.write({'state': 'closed'})
        return True

    @api.multi
    def action_cancel(self):
        prod_obj = self.env['mrp.production']
        proc_obj = self.env['procurement.order']
        # purchase_obj = self.env['purchase.order']
        for order in self:
            for pick in order.picking_ids:
                if pick.state in ['done']:
                    raise UserError(_("The sales order cannot be canceled. \
                        Please close it"))
            production = prod_obj.search([('sale_id', '=', order.id)])
            for prod in production:
                if prod.state in ['in_production', 'done']:
                    raise UserError(_("The sales order cannot be canceled. \
                        Please close it"))
            procurement = proc_obj.search([('sale_id', '=', order.id)])
            for proc in procurement:
                if proc.state in ['done']:
                    raise UserError(_("The sales order cannot be canceled. \
                        Please close it"))
            # purchase = purchase_obj.search([('origin', 'like', order.name)])
            # for purc in purchase:
            #    if purc.state not in ['draft']:
            #        raise UserError(_("The sales order cannot be canceled. \
            #            Please close it"))
        self.all_cancel()
        super(SaleOrder, self).action_cancel()


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
    ], related='order_id.state',
        string=_('Order Status'),
        readonly=True,
        copy=False,
        store=True,
        default='draft')

    # INCOMPLETO
    # @api.multi
    # def action_closed_line(self):
    #     proc_obj = self.env['procurement.order']
    #     move_obj = self.env['stock.move']
    #     for line in self:
    #         if line.order_id.invoice_status == 'invoiced':
    #             raise UserError(_("No se puede Cerrar esta Linea de Venta"
    #                               " el Pedido ya esta Facturado"))
    #         procurement = proc_obj.search([('sale_line_id', '=', line.id)])
    #         if procurement.state in ['confirmed', 'exception', 'running']:
    #                 self.env.cr.execute("""UPDATE procurement_order SET state = 'cancel'
    #                                 WHERE id = %s """ % (procurement.id))
    #         moves = move_obj.search([('procurement_id', '=', procurement.id)])
    #         for move in moves:
    #             _logger.error("stock.move" + str(move.id))
    #             move.procurement_searh()
    #     self.write({'state': 'closed'})

    #     return
