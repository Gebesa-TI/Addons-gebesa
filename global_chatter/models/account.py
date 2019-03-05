# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment', 'message.post.show.all']

class AccountAccount(models.Model):
    _name = 'account.account'
    _inherit = ['account.account', 'mail.thread', 'message.post.show.all']

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'mail.thread', 'message.post.show.all']

class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'message.post.show.all']
