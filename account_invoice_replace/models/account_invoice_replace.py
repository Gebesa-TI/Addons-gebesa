# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from openerp import _, api, fields, models
from openerp.exceptions import UserError, ValidationError


class AccountInvoice(models.Model):

    _name = 'account.invoice'
    _inherit = 'account.invoice'

    invoice_replaced = fields.Many2one(
        'account.invoice',
        string=_("Invoice that replaces"),
    )

    date_cancelled = fields.Date(
        string=_("Cancellation Date"),
    )

    @api.multi
    def action_cancel(self):
        for inv in self:
            if inv.id == inv.invoice_replaced.id:
                raise UserError(_("Please select an invoice to substitute different to the invoice to be canceled"))
            inv.date_cancelled = fields.Date.today()
        return super(AccountInvoice, self).action_cancel()

    @api.model
    def send_email_invoice_canceled(self):
        limit_date = timedelta(days=1)
        date_today_ = fields.Date.today()
        dd = fields.Datetime.from_string(date_today_)
        date_cancel = dd - limit_date
        inv_ids = self.search([
            ('state', '=', ['cancel']),
            ('type', '=', 'out_invoice'),
            ('date_cancelled', '=', date_cancel)])
        table = ''
        remp_date = ''
        remp_rep = ''
        for inve in inv_ids:
            if not inve.date_cancelled:
                remp_date = '---'
            else:
                remp_date = inve.date_cancelled
            if not inve.invoice_replaced:
                remp_rep = '---'
            else:
                remp_rep = inve.invoice_replaced.number
            table += """
                <tr><td style="border-bottom: 1px solid silver;">%s</td>
                    <td style="border-bottom: 1px solid silver;">%s</td>
                    <td style="border-bottom: 1px solid silver;">%s</td>
                    <td align="right" style="border-bottom: 1px solid silver;">
                    %s</td></tr>
            """ % (remp_date, inve.partner_id.name, inve.number, remp_rep)
        mail_obj = self.env['mail.mail']
        body_mail = u"""
            <div summary="o_mail_notification" style="padding:0px; width:700px;
             margin:0 auto; background: #FFFFFF repeat top /100%%; color:#77777
             7">
                <table cellspacing="0" cellpadding="0" style="width:700px;
                border-collapse:collapse; background:inherit; color:inherit">
                    <tbody><tr>
                        <td valign="center" width="270" style="padding:5px 10px
                         5px 5px;font-size: 18px">
                            <p>Las siguientes facturas ya fueron canceladas</p>
                        </td>
                        <td valign="center" align="right" width="270"
                        style="padding:5px 15px 5px 10px; font-size: 12px;">
                            <p>
                            <strong>Sent by</strong>
                            <a href="http://erp.portalgebesa.com" style="text-
                            decoration:none; color: #a24689;">
                                <strong>%s</strong>
                            </a>
                            <strong>using</strong>
                            <a href="https://www.odoo.com" style="text-
                            decoration:none; color: #a24689;"><strong>Odoo
                            </strong></a>
                            </p>
                        </td>
                    </tr>
                </tbody></table>
            </div>
            <div style="padding:0px; width:700px; margin:0 auto; background:
            #FFFFFF repeat top /100%%; color:#777777">
                <table cellspacing="0" cellpadding="0" style="vertical-align:
                top; padding:0px; border-collapse:collapse; background:inherit;
                 color:inherit">
                    <tbody><tr>
                        <td valign="top" style="width:700px; padding:5px 10px
                        5px 5px; ">
                            <div>
                                <hr width="100%%" style="background-color:
                                rgb(204,204,204);border:medium none;clear:both;
                                display:block;font-size:0px;min-height:1px;
                                line-height:0;margin:15px auto;padding:0">
                            </div>
                        </td>
                    </tr></tbody>
                </table>
            </div>
            <div style="padding:0px; width:700px; margin:0 auto; background:
            #FFFFFF repeat top /100%%;color:#777777">
                <table style="border-collapse:collapse; margin: 0 auto; width:
                700px; background:inherit; color:inherit">
                    <tbody><tr>
                        <th width="16%%" style="padding:5px 10px 5px 5px;font-
                        size: 14px; border-bottom: 2px solid silver;"><strong>
                        Fecha de Cancelacion</strong></th>
                        <th width="54%%" style="padding:5px 10px 5px 5px;font-
                        size: 14px; border-bottom: 2px solid silver;"><strong>
                        Cliente</strong></th>
                        <th width="15%%" style="padding:5px 10px 5px 5px;font-
                        size: 14px; border-bottom: 2px solid silver;"><strong>
                        Factura Cancelada</strong></th>
                        <th width="15%%" style="padding:5px 10px 5px 5px;font-
                        size: 14px; border-bottom: 2px solid silver;"><strong>
                        Factura que Sustituye</strong></th>
                    </tr>
                    %s
                    </tbody>
                </table>
            </div>
          """ % (self.env.user.company_id.name, table)
        mail = mail_obj.create({
            'subject': 'Facturas Canceladas',
            'email_to': 'mayte.valdes@gebesa.com,andrea.mejia@gebesa.com,monica.sanchez@gebesa.com,federico.yanez@gebesa.com,jesus.castrellon@gebesa.com,cristina.rodriguez@gebesa.com,esmeralda.gutierrez@gebesa.com,sistemas@gebesa.com',
            'headers': "{'Return-Path': u'odoo@gebesa.com'}",
            'body_html': body_mail,
            'auto_delete': True,
            'message_type': 'comment',
            'model': 'account.invoice',
            'res_id': inv_ids[0].id,
        })
        mail.send()
