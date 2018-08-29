# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError, ValidationError

class AccountInvoiceWizardEvi(models.TransientModel):
    _name = 'account.invoice.wizard.evi'

    @api.multi
    def button_invoice_evidence_wizard(self):
    	invoice_obj = self.env['account.invoice']
    	active_ids = self._context.get('active_ids', []) or []
    	invoice_var = invoice_obj.browse(active_ids)
    	if any (inv.state != 'open' for inv in invoice_var):
    		raise UserError(_("Solo puedes aprobar evidencias para facturas abiertas"))
    	if any(inv.partner_id.id != 2503 for inv in invoice_var):
    		raise UserError(_("Solo puedes aprobar evidencias de facturas de Transportes Galbo"))	
    	for inv in invoice_var:
    		inv.evidence_status = 'received'
