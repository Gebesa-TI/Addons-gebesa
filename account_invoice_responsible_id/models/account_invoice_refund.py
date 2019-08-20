# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models
from openerp.exceptions import UserError


class AccountInvoiceRefund(models.Model):
    _inherit = 'account.invoice.refund'

    replacement = fields.Boolean(
        string=_('Replacement'),
    )

    responsible_id = fields.Many2one(
        'res.users',
        string=_('Responsible'),
    )


