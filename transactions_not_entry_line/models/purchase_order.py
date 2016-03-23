# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models
from openerp.exceptions import UserError


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    def button_confirm(self, cr, uid, ids, context=None):
        for po in self.browse(cr, uid, ids, context=context):
            if not po.order_line:
                raise UserError(_('You cannot confirm a purchase order without \
                 any purchase order line.'))
            for line in po.order_line:
                if line.price_unit <= 0:
                    raise UserError(_('At least one of the lines of the \
                    purchase order has price unit zero!' '\n Please make sure \
                    that all lines have successfully captured the unit price.')
                                    )

        return super(PurchaseOrder, self).button_confirm(
            cr, uid, ids, context=context)
