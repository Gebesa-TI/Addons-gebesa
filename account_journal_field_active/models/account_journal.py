# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    active = fields.Boolean(
        string=_('Active'),
        default=True,
    )
