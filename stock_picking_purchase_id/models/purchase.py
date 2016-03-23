# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    @api.model
    def _prepare_picking(self):
        purchase_vals = super(PurchaseOrder, self)._prepare_picking()
        purchase_vals['purchase_id'] = self.id

        return purchase_vals
