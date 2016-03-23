# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta
from openerp import _, fields, models, api
from openerp.exceptions import UserError


class AccountPayment(models.Model):
    _name = "account.payment"
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        """ Create the movements to the given date,
        according to the days of tolerance granted to the user"""
        employee_days = self.env['hr.employee'].search(
            [('user_id', '=', self._uid)])[1].tolerance_days

        for rec in self:
            if rec.payment_date is not False:
                days_tol = str(date.today() - timedelta(days=employee_days))
                if rec.payment_date < days_tol:
                    raise UserError(_('Error! \
                                    The date may not be earlier \
                                    than %s .') % days_tol)

        return super(AccountPayment, self).post()
