# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    advance_id = fields.Many2one(
        'account.invoice',
        string=_('Advance Invoice'),
    )

    amount_advance = fields.Float(
        _('Amount Advance'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_amount_adv',
        store=True,
    )

    advance_ids = fields.One2many(
        'account.invoice.rel.advance',
        'invoice_id',
        string=(_('Advance')),
    )

    @api.onchange('advance_id')
    def _onchange_advance_id(self):
        advance = self.advance_id
        if advance:
            if advance.amount_residual_advance >= self.amount_total:
                self.amount_advance = self.amount_total
            else:
                self.amount_advance = advance.amount_residual_advance
        return

    #@api.depends('advance_id')
    #def _compute_amount_adv(self):
        #if self.advance_id:
            #self.amount_advance = self.advance_id.amount_total


    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        for partner in self:
            partner.advance_ids = ''

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.prepayment_move_ids:
                advance_invoice_ids = self.prepayment_move_ids.mapped(
                    'line_ids').mapped('invoice_id')
                l10n_mx_edi_origin = '07|'
                for advance_invoice in advance_invoice_ids:
                    advance_invoice.advance_applied = True
                    l10n_mx_edi_origin += advance_invoice.cfdi_uuid + ','
                inv.l10n_mx_edi_origin = l10n_mx_edi_origin[:-1]
            elif inv.advance_id:
                inv.advance_id.advance_applied = True
                inv.l10n_mx_edi_origin = '07|' + inv.advance_id.cfdi_uuid
            elif inv.advance_ids:
                total_advance = 0.0
                resta = 0.0
                inv.l10n_mx_edi_origin = '07|'
                for advance in inv.advance_ids:
                    if advance.advance_id:
                        if not advance.amount_advance > advance.advance_id.amount_residual_advance:
                            resta = advance.advance_id.amount_residual_advance - advance.amount_advance
                            advance.advance_id.amount_residual_advance = resta
                            if advance.advance_id.amount_residual_advance == 0.0:
                                advance.advance_id.advance_applied = True
                        else:
                            raise UserError('El monto de anticipo es mayor al saldo de la factura %s' % advance.advance_id.number)
                        total_advance += advance.amount_advance
                        inv.l10n_mx_edi_origin += str(advance.advance_id.cfdi_uuid) + ','
                    else:
                        raise UserError('El monto necesita un anticipo')
                
                if total_advance > self.amount_total:
                    raise UserError('La sumatoria de las facturas de anticipo es mayor que el monto total de esta facturas')        
                inv.l10n_mx_edi_origin = inv.l10n_mx_edi_origin[:-1]

            # if inv.advance_id and not inv.advance_id.sale_id:
            #     adv_id = inv.advance_id
            #     prod_adv = False
            #     tax_prod = []
            #     for line in adv_id.invoice_line_ids:
            #         deposit = self.pool['ir.values'].get_default(
            #             self._cr, self._uid, 'sale.config.settings',
            #             'deposit_product_id_setting') or False
            #         if line.product_id.id == deposit:
            #             product = self.env['product.product'].search(
            #                 [('id', '=', deposit)])
            #             prod_adv = product
            #             tax_prod = [(6, 0, [x.id for x in
            #                          line.product_id.taxes_id])]

            #     if not prod_adv:
            #         raise UserError(_('The Advance Invoice to which it refers,'
            #                           '\n does not have an Article type'
            #                           'in Advance'))

            #     inv_line_values2 = {
            #         'name': _('Aplication of advance'),
            #         'origin': inv.advance_id.number,
            #         'account_id': prod_adv.property_account_income_id.id,
            #         'price_unit': inv.amount_advance * -1,
            #         'quantity': 1.0,
            #         'discount': False,
            #         'uom_id': prod_adv.uom_id.id or False,
            #         'product_id': prod_adv.id,
            #         'invoice_line_tax_id': tax_prod,
            #         'account_analytic_id': inv.account_analytic_id.id,
            #         'invoice_id': inv.id,
            #     }
            #     inv_line_obj = self.env['account.invoice.line']
            #     inv_line_id = inv_line_obj.create(inv_line_values2)

            #     inv.advance_id.advance_applied = True

        return res
