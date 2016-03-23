# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp.exceptions import UserError


class FactoringCustomer(models.Model):
    _name = 'factoring.customer'
    _inherit = ['mail.thread']
    _description = "Factoring Customer"
    _order = 'consecutive asc'
    _rec_name = 'consecutive'

    consecutive = fields.Char(
        string=_(u'Folio'),
        size=250,
        required=True,
        select=True,
        copy=False,
        default='New',
        track_visibility='always')

    reference = fields.Char(
        string=_('Reference'),
        size=250,
        track_visibility='onchange')

    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
        track_visibility='onchange')

    journal_id = fields.Many2one(
        'account.journal',
        string=_(u'Bank'),
        domain="[('type', 'in', ('bank','cash'))]",
        track_visibility='onchange')

    company_id = fields.Many2one(
        'res.company',
        string=_(u'Company'),
        default=lambda self: self.env['res.company']._company_default_get(
            'factoring.customer'),
        track_visibility='always')

    date = fields.Date(
        string=_(u'Date'),
        default=fields.Date.today,
        track_visibility='always')

    invoice_ids = fields.Many2many(
        'account.invoice',
        string=_(u'Customer Invoices'),
        track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        string=_(u'Status'),
        track_visibility='onchange',
        default='draft')

    date_bank = fields.Date(
        string=_(u'Payment Date the Bank'),
        track_visibility='always')

    _sql_constraints = [
        ('consecutive_uniq', 'unique (consecutive)',
         'This field must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('consecutive', 'New') == 'New':
            vals['consecutive'] = self.env['ir.sequence'].next_by_code(
                'factoring.customer') or '/'
        return super(FactoringCustomer, self).create(vals)

    def integrated_factoring(self, _cr, _uid, _ids, _context=None):
        ids = isinstance(_ids, (int, long)) and [_ids] or _ids
        inv_obj = self.pool.get('account.invoice')
        int_brw = self.browse(_cr, _uid, ids[0], context=_context)
        res = []
        res.append(int_brw.invoice_ids and True or False)
        if not all(res):
            raise UserError(_('You can not perform factoring! \
                                    You must select at leats one bill.'))
        for inv_brw in int_brw.invoice_ids:
            inv_obj.write(_cr, _uid, [
                          inv_brw.id], {'factoring_customer_id': int_brw.id},
                          context=_context)
        self.write(_cr, _uid, [int_brw.id], {'state': 'done'},
                   context=_context)

        return res
