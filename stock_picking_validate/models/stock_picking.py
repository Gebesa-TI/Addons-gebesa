# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    authorized = fields.Boolean(
        string=_('Autorizar'),
    )

    @api.multi
    def button_stock_picking(self):
        self.authorized = True

    @api.multi
    def do_new_transfer(self):
        for stock in self:
            origin = stock.location_id.usage
            destin = stock.location_dest_id.usage
            if origin == 'inventory' or destin == 'inventory':
                if not self.authorized:
                    raise UserError(_("Missing authorization module to be validated"))
                if not self.env.user.has_group(
                        'stock_picking_validate.group_button_validate_adjustment'):
                    raise UserError(
                        _('Error!\nDoes not count on provilegios to validate this exit by adjustment.'))
        return super(StockPicking, self).do_new_transfer()
