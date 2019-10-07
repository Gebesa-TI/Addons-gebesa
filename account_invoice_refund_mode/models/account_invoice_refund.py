# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.exceptions import UserError


class AccountInvoiceRefund(models.Model):
    _inherit = 'account.invoice.refund'

    @api.multi
    def compute_refund(self, mode='refund'):
        context = dict(self._context or {})
        context.update({'mode': mode})
        invoice = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        invoice.mode = mode

        deposit = self.pool['ir.values'].get_default(
            self._cr, self._uid, 'sale.config.settings',
            'deposit_product_id_setting') or False
        total_advance = 0.0
        if self.filter_refund == 'refund':
            if self.product_id.id == deposit:
                for advance in invoice.advance_ids:
                    total_advance += advance.amount_advance
                if abs(total_advance - self.amount) > 0.50:
                    raise UserError('Debe aplicar el total de los anticipos')

                invoice.note_applied = True

        res = super(AccountInvoiceRefund, self).compute_refund(invoice.mode)
        return res
