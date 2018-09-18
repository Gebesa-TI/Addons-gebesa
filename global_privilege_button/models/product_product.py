# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_product'):
            raise UserError(_('Error!\nYou do not have privileges to Create'
                              ' Product(s).\nCheck with your'
                              ' System Administrator.'))
        if 'is_line' in vals.keys():
            if vals.get('is_line') is True and \
               not self.env.user.has_group('global_privilege_button.group_manager_is_line_product'):
                raise UserError(_('Error!\nYou do not have privileges to Create'
                                  ' Line Products.'))
        return super(ProductProduct, self).create(vals)

    @api.one
    def write(self, vals):
        bom_line_obj = self.env['mrp.bom.line']
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_product'):
            raise UserError(_('Error!\nYou do not have privileges to Modify'
                              ' Product(s).\nCheck with your'
                              ' System Administrator.'))
        if 'active' in vals.keys():
            bom_line_ids = bom_line_obj.search([('product_id', '=', self.id)])
            bom_ids = bom_line_ids.mapped('bom_id').filtered(
                lambda x: x.active is True)
            if vals.get('active') is False and len(bom_ids) > 0:
                raise UserError(_('Error!\nNo puede Inactivar un Producto que'
                                  ' se encuentra en listas de materiales activas.'))
            if vals.get('active') is False and self.qty_available != 0:
                raise UserError(_('Error!\nNo puede Inactivar un Producto con'
                                  ' existencia en el Sistema.'))
        # reference_mask,attribute_line_ids,name,sale_ok,purchase_ok,type,default_code,product_service_id,is_line,family_id,group_id,line_id,route_ids,categ_id,tracking,invoice_policy,description_sale,standard_price
        criticalFields = {'reference_mask', 'attribute_line_ids',
                          'name', 'sale_ok', 'purchase_ok', 'type',
                          'product_service_id', 'is_line', 'family_id',
                          'group_id', 'line_id', 'route_ids', 'categ_id',
                          'tracking', 'invoice_policy',
                          'description_sale', 'standard_price', 'default_code'}

        needVal = False
        for field in criticalFields:
            if field in vals.keys():
                needVal = True

        # if len(vals.keys()) > 0:
        if needVal:
            if 'is_line' in vals.keys() and not self.env.user.has_group(
                    'global_privilege_button.group_manager_is_line_product'):
                raise UserError(_('Error!\nYou do not have privileges \
                                to Set Line Products.'))

            if self.is_line is True and not self.env.user.has_group(
                    'global_privilege_button.group_manager_is_line_product'):
                raise UserError(_('Error!\nYou do not have privileges \
                                to Modify Line Products.\n You are \
                                modifying: %s') % (vals))
        return super(ProductProduct, self).write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_product'):
            raise UserError(_('Error!\nYou do not have privileges to Delete'
                              ' Product(s).\nCheck with your'
                              ' System Administrator.'))
        return super(ProductProduct, self).unlink()
