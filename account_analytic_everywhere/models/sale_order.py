# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):

        res = super(SaleOrder, self).action_invoice_create(
            grouped, final)
        invoice = self.env['account.invoice'].browse(res)
        for inv in invoice:
            inv.account_analytic_id = inv.sale_id.project_id
            inv.journal_id = inv.sale_id.project_id.journal_sale_id
        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        product_obj = self.env['product.product']
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        product_id = product_obj.browse(int(res['product_id']))
        analytic_id = product_id.family_id.analytic_id
        if analytic_id:
            res['account_analytic_id'] = analytic_id.id
        return res

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        for inv in res:
            inv.account_analytic_id = order.project_id
        return res
