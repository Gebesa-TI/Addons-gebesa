# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models

class TransferReq(models.Model):
    _name = 'transfer.req'
    _description = 'transfer'
    _rec_name = 'name'

    name = fields.Char(
        string='Transferencias:',
        required=True,
        )

    color = fields.Integer()

    name_cheke = fields.Char(
        string='Cheque:',
        )

    responsible_id = fields.Many2one('hr.employee',
        ondelete='set null', string="Solicitud de:", index=True)

    date = fields.Date(
        string=_('Date'),
        default=fields.Date.today,
        track_visibility='always')

    Traspaso = fields.Boolean(default=True, required=True)

    company_id = fields.Many2one('res.company',
        ondelete='set null', string="Empresa:", index=True)

    bank_id = fields.Many2one('res.bank',
        ondelete='set null', string="Banco:", required=True, index=True)
    
    emp_ven_id = fields.Many2one('res.partner',
        ondelete='set null', string="A favor de:", index=True)

    cantidad = fields.Float(required=True, digits=(6, 2))

    con_obs = fields.Text(
            string='Concepto y Obs:',
        )

    facturar_a = fields.Many2one('res.company',
        ondelete='set null', string="Facturar a:", index=True)

    cantidad_fac = fields.Float(required=True, digits=(6, 2) , string="Cantidad a facturar")
    
    gasto_id =fields.Many2one('hr.employee',
        ondelete='set null', string="Gasto para: ", index=True)
