# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models , _ , api 
from openerp.exceptions import UserError, ValidationError

class CursoPrueba(models.Model):
    _name = 'curso.prueba'
    _description = 'curso'
    _rec_name = 'name'

    name = fields.Char(
        string='Nombre de Curso',
        required=True,
        )

    description = fields.Text(
    		string='description',
        )
    responsible_id = fields.Many2one('res.users',
         ondelete='set null', string="Responsible", index=True)

    status_course = fields.Selection(
        [('finalized', _('Finalized')),
         ('not_finalized', _('Not Finalized'))],
        string=_('Estatus del curso'),
        default='not_finalized'
        )

    @api.multi
    def button_course_stauts(self):
        for rec in self:
            rec.write({'status_course': 'finalized'})
        return True

class SessionPrueba(models.Model):
    _name = 'session.prueba'

    course_id = fields.Many2one('curso.prueba',
        ondelete='cascade', string="Course", required=True)
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    attendee_ids = fields.Many2many('res.partner', string="Número de personas que asistieron")
    seats = fields.Integer(string="Número de asientos")
    sessions_taken = fields.Float(string="Asientos tomadas", compute='_sessions_taken')
    active = fields.Boolean(default=True)
    color = fields.Integer()

    status_session = fields.Selection(
        [('finished', _('Finializada')),
         ('not_finished', _('No Finalizada'))],
        string=_('Estatus de la Sesiòn'),
        default='not_finished'
        )

    @api.multi
    def write (self, vals):
        import ipdb; ipdb.set_trace()
        for rec in self:
            if rec.seats < 0: 
                raise UserError(_("La cantidad de asientos disponibles puede no ser negativa"))
            if vals['seats'] < len(rec.attendee_ids):
                raise UserError(_("Aumenta los asientos o elimina el exceso de asistentes"))
        return super(SessionPrueba, self).write(vals) 

    @api.multi
    def button_session_status(self):
        for rec in self:
            rec.write({'status_session': 'finished'})
        return True

    @api.depends('seats', 'attendee_ids')
    def _sessions_taken(self):
        for r in self:
            if not r.seats:
                r.sessions_taken = 0.0
            else:
                r.sessions_taken = 100.0 * len(r.attendee_ids) / r.seats
  
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "La cantidad de asientos disponibles puede no ser negativa",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Aumenta los asientos o elimina el exceso de asistentes",
                },
            }
