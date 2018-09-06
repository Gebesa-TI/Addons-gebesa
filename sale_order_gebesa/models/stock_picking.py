# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):
        for pick in self:
            if pick.location_dest_id.usage != 'customer':
                continue
            if not pick.sale_id:
                continue
            if pick.sale_id.not_be_billed:
                raise UserError(
                    _('This Sales Order is not invoiced'))
        return super(StockPicking, self).do_new_transfer()

    @api.model
    def _prepare_values_extra_move(self, op, product, remaining_qty):
        raise UserError(
            _('Favor de contactar al admistador del sistema. \n \
                Esta tansferencia creara movimientos extras'))
        return super(StockPicking, self)._prepare_values_extra_move(op, product, remaining_qty)
