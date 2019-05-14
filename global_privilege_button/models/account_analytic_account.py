# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group(
                'global_privilege_button.group_global_privilege_account'):
            raise UserError(_('Error!\nYou do not have privileges to Create'
                              ' Analytic(s) account.\nCheck with your'
                              ' System Administrator.'))
        return super(AccountAnalyticAccount, self).create(vals)

    @api.one
    def write(self, vals):
        if not self.env.user.has_group(
                'global_privilege_button.group_global_privilege_account'):
            raise UserError(_('Error!\nYou do not have privileges to Modify'
                              ' Analytic(s) account.\nCheck with your'
                              ' System Administrator.'))
        return super(AccountAnalyticAccount, self).write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'global_privilege_button.group_global_privilege_account'):
            raise UserError(_('Error!\nYou do not have privileges to Delete'
                              ' Analytic(s) account.\nCheck with your'
                              ' System Administrator.'))
        return super(AccountAnalyticAccount, self).unlink()
