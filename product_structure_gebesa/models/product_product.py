# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    individual_name = fields.Char(
        string=_('Individual name'),
        translate=True,
    )
    name_template = fields.Char(
        string=_('Template Name'),
        store=True,
        compute='compute_name_template',
    )

    quotation_product = fields.Boolean(
        string=_('Quotation Product'),
    )

    @api.multi
    def propagar_peso_volumen_variantes(self):
        for product in self:
            self._cr.execute(
                """UPDATE product_product SET
                    volume = %s,
                    weight = %s
                    WHERE product_tmpl_id = %s
                        AND active IS TRUE""",
                (product.volume, product.weight, product.product_tmpl_id.id))

    @api.depends('product_tmpl_id.name', 'individual_name')
    def compute_name_template(self):
        for prod in self:
            if prod.individual_name:
                prod.name_template = prod.individual_name
            elif prod.product_tmpl_id.name:
                prod.name_template = prod.product_tmpl_id.name
            else:
                prod.name_template = ''

    @api.multi
    def create(self, vals):
        if 'default_code' in vals:
            vals['barcode'] = vals['default_code']
        return super(ProductProduct, self).create(vals)

    @api.one
    def write(self, values):
        if 'default_code' in values:
            values['barcode'] = values['default_code']
        else:
            values['barcode'] = self.default_code
        return super(ProductProduct, self).write(values)

    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get(
                'display_default_code', True) and d.get(
                'default_code', False) or False
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        partner_id = self._context.get('partner_id', False)
        if partner_id:
            partner_ids = [
                partner_id,
                self.env['res.partner'].browse(
                    partner_id).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for product in self:
            if product.individual_name:
                if product.default_code:
                    name = '[%s] %s' % (
                        product.default_code, product.individual_name)
                else:
                    name = product.individual_name
                result.append((product.id, name))
            else:
                variant = ", ".join(
                    [v.name for v in product.attribute_value_ids])
                name = variant and "%s (%s)" % (
                    product.name, variant) or product.name
                sellers = []
                if partner_ids:
                    sellers = [x for x in product.seller_ids if (
                        x.name.id in partner_ids) and (
                        x.product_id == product)]
                    if not sellers:
                        sellers = [x for x in product.seller_ids if (
                            x.name.id in partner_ids) and not x.product_id]
                if sellers:
                    for s in sellers:
                        seller_variant = s.product_name and (
                            variant and "%s (%s)" % (
                                s.product_name, variant) or s.product_name
                        ) or False
                        mydict = {
                            'id': product.id,
                            'name': seller_variant or name,
                            'default_code': s.product_code or product.default_code,
                        }
                        temp = _name_get(mydict)
                        if temp not in result:
                            result.append(temp)
                else:
                    mydict = {
                        'id': product.id,
                        'name': name,
                        'default_code': product.default_code,
                    }
                    result.append(_name_get(mydict))
        return result
