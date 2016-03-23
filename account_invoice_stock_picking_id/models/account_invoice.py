# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    picking_id = fields.Many2one('stock.picking',
                                 ondelete='restrict',
                                 string=_("Related Picking"),
                                 index=True,
                                 readonly=True)
