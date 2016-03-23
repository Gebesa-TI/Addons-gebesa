# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    @api.multi
    def post(self):
        for move in self:
            journal = move.journal_id
            if journal.active is False:
                raise UserError(_("The Journal %s cannot be used.") % (
                                journal.name))

        return super(AccountMove, self).post()
