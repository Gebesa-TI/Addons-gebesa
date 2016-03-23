# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        for inv in self:
            for line in inv.invoice_line_ids:
                if line.price_unit <= 0:
                    raise UserError(_('At least one of the lines of the \
                    invoice has price unit zero!' '\n Please make sure \
                    that all lines have successfully captured the unit price.')
                                    )

        return super(AccountInvoice, self).action_move_create()
