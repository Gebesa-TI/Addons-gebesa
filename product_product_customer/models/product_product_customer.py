# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api,_ 


class ProductProductCustomer(models.Model):
    _name = 'product.product.customer'
    rec_name = 'client_code'

    customer_code = fields.Char(
        string='Customer Product Code',
        size=64,
    )
    customer_description = fields.Char(
        string='Customer Product Description',
        translate=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    qty = fields.Integer(
        'Quantity',
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_customer_ids = fields.One2many(
        'product.product.customer',
        'product_id',
        string='Customer product',
    )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sku_on_invoices = fields.Boolean(
        string=_('SKU'),
    )


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):

        domain = super(AccountInvoiceLine, self)._onchange_product_id()
        part = self.invoice_id.partner_id
        product = self.product_id

        if part.sku_on_invoices and product:
            ppc_ids = self.env['product.product.customer'].search([('partner_id', '=', part.id),('product_id', '=', product.id)], limit=1)
            if ppc_ids:
                self.name = 'SKU: ' + ppc_ids.customer_code + ' \n' + self.name

        return domain


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):

        domain = super(SaleOrderLine, self).product_id_change()
        partner = self.order_partner_id
        product = self.product_id

        if partner.sku_on_invoices and product:
            ppc_ids = self.env['product.product.customer'].search([('partner_id', '=', partner.id),('product_id', '=', product.id)], limit=1)
            if ppc_ids:
                self.name = 'SKU: ' + ppc_ids.customer_code + ' \n' + self.name

        return domain
