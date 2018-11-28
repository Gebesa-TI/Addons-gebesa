# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u'Analytic Account'),
    )

    @api.multi
    def action_date_assign(self):
        res = super(AccountInvoice, self).action_date_assign()
        for inv in self:
            if inv.type in ('in_invoice', 'in_refund'):
                continue
            for line in inv.invoice_line_ids:
                if not line.account_analytic_id:
                    line.account_analytic_id = inv.account_analytic_id.id
        return res

    @api.model
    def line_get_convert(self, line, part):
        res = super(AccountInvoice, self).line_get_convert(line, part)
        if not res['analytic_account_id'] and self.type in (
                'out_invoice', 'out_refund'):
            res['analytic_account_id'] = self.account_analytic_id.id
        return res

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.type in ('in_invoice'):
                inv.asigna_analytic()
        return res

    def asigna_analytic(self):
        move = self.move_id

        for line in move.line_ids:
            if not line.analytic_account_id:
                line.analytic_account_id = self.account_analytic_id

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        if not self.purchase_id:
            return {}
        self.account_analytic_id = self.purchase_id.account_analytic_id.id


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def _set_additional_fields(self, invoice):
        analytic = self.account_analytic_id
        super(AccountInvoiceLine, self)._set_additional_fields(invoice)
        self.account_analytic_id = analytic

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine, self)._onchange_product_id()
        for line in self:
            analytic_id = line.invoice_id.account_analytic_id.id
            if line.invoice_id.type in ('out_invoice', 'out_refund'):
                if line.product_id:
                    product_tmpl_id = line.product_id.product_tmpl_id
                    if product_tmpl_id.type != 'service':
                        if not product_tmpl_id.family_id:
                            raise ValidationError(_(
                                "El producto %s no tiene familia asignada") %
                                line.product_id.default_code)
                        if not product_tmpl_id.family_id.analytic_id:
                            raise ValidationError(_(
                                "La familia %s no tiene asignada una cuenta analitica") %
                                product_tmpl_id.family_id.name)
                        analytic_id = product_tmpl_id.family_id.analytic_id.id
            line.account_analytic_id = analytic_id
        return res
