# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models

class AccountInvoiceRelAdvance(models.Model):
    _name = 'account.invoice.rel.advance'

    invoice_id = fields.Many2one(
        'account.invoice',
        string=(_('Invoice')),
    )
    advance_id = fields.Many2one(
        'account.invoice',
        string=(_('Advance')),
    )
    amount_advance = fields.Float(
        string=(_('Amount Advance')),
    )

    @api.onchange('advance_id')
    def _onchange_advance_id(self):
        advance = self.advance_id
        if advance:
            if advance.amount_residual_advance >= self.invoice_id.amount_total:
                self.amount_advance = self.invoice_id.amount_total
            else:
                self.amount_advance = advance.amount_residual_advance
        return