# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api,exceptions, _, fields, models
from openerp.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    # _name = 'account.payment'
    _inherit = 'account.payment'

    @api.multi
    def post (self):
        for rec in self:
            if any(inv.partner_id.id == 2503 and inv.evidence_status != 'received' for inv in rec.invoice_ids):
               raise UserError(_("El pago no puede ser confirmado porque algunas facturas no tienen evidencias aprobadas"))
        return super(AccountPayment, self).post()
