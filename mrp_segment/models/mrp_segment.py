# -*- coding: utf-8 -*-
# © <2016> <Cesar Barron>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
import datetime
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError


class MrpSegment(models.Model):
    _name = "mrp.segment"
    _inherit = ['mail.thread']
    _description = "MRP Segment"
    _rec_name = 'folio'

    def _default_stock_location(self):
        try:
            warehouse = self.env['ir.model.data'].get_object(
                'stock', 'warehouse0')
            return warehouse.lot_stock_id.id
        except:
            return False

    name = fields.Char(
        string=_('Segment Reference'),
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='always',
        help=_('Segment Name.'))

    folio = fields.Char(
        string='Folio',
        required=True,
        readonly=True,
        copy=False,
        track_visibility='always',
        default='new',
    )

    date = fields.Datetime(
        string=_('Segment Date'),
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        help=_('The date that will be used for the segment.'))

    state = fields.Selection(
        [('draft', 'Draft'),
         ('cancel', 'Cancelled'),
         ('construction', 'In Construction'),
         ('confirm', 'In Progress'),
         ('done', 'Validated')],
        string=_('Status'),
        readonly=True,
        select=True,
        default='draft',
        track_visibility='onchange',
        copy=False)

    location_id = fields.Many2one(
        'stock.location',
        string=_('Segment Location'),
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
        default=_default_stock_location)

    company_id = fields.Many2one(
        'res.company',
        string=_('Company'),
        required=True,
        select=True,
        readonly=True,
        default=lambda self: self.env.user.company_id,
        states={'draft': [('readonly', False)]})

    line_ids = fields.One2many(
        'mrp.segment.line',
        'segment_id',
        string=_('Manufacturing Order Line'),
        readonly=False,
        states={'done': [('readonly', True)]},
        help=_("Segment Lines."),
        copy=True,
        ondelete='cascade')

    product_lines_ids = fields.One2many(
        'mrp.production.product.line',
        'production_id',
        compute='_compute_product_lines_ids',
        string='Scheduled goods',
    )

    express = fields.Boolean(
        string='Expres'
    )

    commitment_date = fields.Datetime(
        string=_('Commitment Date'),
        track_visibility='onchange',
    )

    commitment_week_number = fields.Integer(
        string=_('Commitment Week Number'),
        track_visibility='onchange',
    )

    progress_date = fields.Date(
        string=_('Progress Date')
    )

    @api.depends('line_ids.mrp_production_id')
    def _compute_product_lines_ids(self):
        product_lines = []
        for line in self.line_ids:
            for pro_lin in line.mrp_production_id.product_lines:
                product_lines.append(pro_lin.id)
        self.product_lines_ids = product_lines

    _sql_constraints = [
        ('folio_uniq', 'unique (folio)',
         'This field must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('folio', 'New') == 'New':
            vals['folio'] = self.env['ir.sequence'].next_by_code(
                'mrp.segment') or '/'
        # campo = fields.Datetime.now()
        # if 'commitment_date' in vals.keys():
        #     campo = str(vals['commitment_date'])
        # arreglo = campo.split(" ")
        # arreglo2 = arreglo[0].split("/")
        # cadena_n = ("-").join(arreglo2)
        # week_number = int(datetime.datetime.strptime(
        #     cadena_n, '%Y-%m-%d').strftime('%W'))
        # vals['commitment_week_number'] = week_number
        return super(MrpSegment, self).create(vals)

    @api.multi
    def write(self, values):
        if self._uid != self.create_uid.id:
            raise UserError(_('You can not modify this segment'))
        if 'commitment_date' in values.keys():
            campo = str(values['commitment_date'])
            arreglo = campo.split(" ")
            arreglo2 = arreglo[0].split("/")
            cadena_n = ("-").join(arreglo2)
            week_number = int(datetime.datetime.strptime(
                cadena_n, '%Y-%m-%d').strftime('%W'))
            values['commitment_week_number'] = week_number
        return super(MrpSegment, self).write(values)

    @api.multi
    def unlink(self):
        for segment in self:
            if self._uid != segment.create_uid.id:
                raise UserError(_('You can not delete this segment'))
        return super(MrpSegment, self).unlink()

    @api.multi
    def prepare_segment(self):
        for segment in self:
            line_ids = [line.id for line in segment.line_ids]
            if not line_ids:
                vals = self._get_segment_lines()

                for production_line in vals:
                    self.env['mrp.segment.line'].create(production_line)

        return self.write({'state': 'construction'})

    def _get_segment_lines(self):
        domain = [('segment_line_ids', '=', False),
                  ('location_dest_id', '=', self.location_id.id),
                  ('state', 'in', ["confirmed", "ready"])]

        segment_lines = self.env['mrp.production'].search(domain)

        vals = []
        for produ in segment_lines:
            product_line = dict(
                (fn, 0.0) for fn in [
                    'segment_id', 'mrp_production_id',
                    'product_id', 'sale_name', 'product_qty',
                    'quantity'])

            product_line['segment_id'] = self.id
            product_line['mrp_production_id'] = produ.id
            product_line['product_id'] = produ.product_id.id
            product_line['sale_name'] = produ.origin
            product_line['product_qty'] = produ.product_qty
            product_line['quantity'] = 0
            vals.append(product_line)
        return vals

    @api.multi
    def process_segment(self):
        produce_obj = self.env['mrp.production']
        for produ in self.line_ids:
            if produ.quantity > 0:
                produce_obj.action_produce(produ.mrp_production_id.id,
                                           produ.quantity,
                                           'consume_produce',
                                           )
        return True

    @api.multi
    def validate_segment(self):
        production_obj = self.env['mrp.production']
        for segment in self:
            for line in segment.line_ids:
                self.env.cr.execute("""UPDATE procurement_order
                        SET related_segment = CONCAT(related_segment, %s )
                        WHERE origin LIKE %s""",
                                    (segment.folio + ', ',
                                     '%' + line.mrp_production_id.name + '%'))
                self.env.cr.execute("""UPDATE stock_picking
                        SET related_segment = CONCAT(related_segment, %s )
                        WHERE origin LIKE %s""",
                                    (segment.folio + ', ',
                                     '%' + line.mrp_production_id.name + '%'))
                self.env.cr.execute(
                    """UPDATE stock_move
                        SET related_segment = CONCAT(related_segment, %s)
                        WHERE origin LIKE %s""",
                    (segment.folio + ', ',
                     '%' + line.mrp_production_id.name + '%'))
                self.env.cr.execute(
                    """UPDATE purchase_order
                        SET related_segment = CONCAT(related_segment, %s)
                        WHERE origin LIKE %s""",
                    (segment.folio + ', ',
                     '%' + line.mrp_production_id.name + '%'))
                sale = line.mrp_production_id.sale_id
                if sale:
                    if not sale.related_segment:
                        self.env.cr.execute(
                            """UPDATE sale_order
                                SET related_segment = %s
                                WHERE id = %s """,
                            (segment.folio + ', ', sale.id)
                        )
                    elif segment.folio not in sale.related_segment:
                        self.env.cr.execute(
                            """update sale_order
                                set related_segment = CONCAT(
                                    related_segment,%s)
                                where id = %s """,
                            (segment.folio + ', ', sale.id)
                        )
                    prod = production_obj.search(
                        [('sale_id', '=', sale.id),
                         ('state', '!=', 'cancel')])
                    prod_seg = production_obj.search(
                        [('sale_id', '=', sale.id),
                         ('state', '!=', 'cancel'),
                         ('segment_line_ids', '!=', False)])
                    if not prod_seg:
                        sale.segment_status = 'no_segment'
                    elif len(prod) == len(prod_seg):
                        sale.segment_status = 'total_segment'
                    else:
                        sale.segment_status = 'partial_segment'
                    segment.progress_date = fields.Datetime.now()
        return self.write({'state': 'confirm'})

    @api.multi
    def cancel_segment(self):
        for line in self.line_ids:
            line.quantity = 0
        for line in self.line_ids:
            line.unlink()
        return self.write({'state': 'cancel'})

    @api.multi
    def add(self):
        ctx = self.env.context.copy()
        ctx.update({'default_location_id': self.location_id.id})
        return {
            'name': 'Add Production',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.segment.add.production',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': ctx,
        }


class MrpSegmentLine(models.Model):
    _name = "mrp.segment.line"
    _description = "Segmentation Line"
    _order = 'segment_id'

    segment_id = fields.Many2one(
        'mrp.segment',
        string=_('Segmentation'),
        ondelete='cascade',
        select=True,
        readonly=True,)

    mrp_production_id = fields.Many2one(
        'mrp.production',
        required=True,
        string=_('Manufacturing Order'),
        readonly=True,
    )

    state = fields.Selection(
        [('draft', _('New')),
         ('cancel', _('Cancelled')),
         ('confirmed', _('Awaiting Raw Materials')),
         ('ready', _('Ready to Produce')),
         ('in_production', _('Production Started')),
         ('done', _('Done'))],
        string=_("Status"),
        readonly=True,
        related='mrp_production_id.state',
    )

    product_id = fields.Many2one(
        'product.product',
        string=_('Product'),
        readonly=True,
    )

    product_code = fields.Char(
        string=_('Code Product'),
        related='product_id.default_code',
        store=True,
        readonly=True,)

    product_name = fields.Char(
        string=_('Name Product'),
        related='product_id.name',
        store=True,
        readonly=True,)

    product_weight = fields.Float(
        string=_('Weight Product'),
        related='product_id.weight',
        store=True,
        readonly=True,)

    product_volume = fields.Float(
        string=_('Volume Product'),
        related='product_id.volume',
        store=True,
        readonly=True,)

    standard_cost = fields.Float(
        string=_('Standard Cost'),
        # compute='_compute_standard_price',
        store=True,
        readonly=True,
    )

    product_uom = fields.Many2one(
        'product.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        readonly=True,
    )

    sale_name = fields.Char(
        string=_('Sale Order'),
        readonly=True,
    )

    product_qty = fields.Float(
        string=_('Product quantity'),
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True,
    )

    manufacture_qty = fields.Float(
        string=_('Quantity to manufacture'),
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True,
    )

    quantity = fields.Float(
        string=_('Done'),
        digits=dp.get_precision('Product Unit of Measure')
    )

    @api.constrains('quantity')
    def _check_qty_segmented(self):
        for line in self:
            if line.quantity > line.manufacture_qty:
                raise UserError(_("The quantity available is less than \n"
                                  "the quantity segmented"))

    @api.model
    def create(self, vals):
        procurement_obj = self.env['procurement.order']
        procurement = procurement_obj.search(
            [('production_id', '=', vals['mrp_production_id'])])
        if procurement.group_id:
            procurements = procurement_obj.search(
                [('group_id', '=', procurement.group_id.id),
                 ('state', 'in', ['exception', 'confirmed'])])
            if len(procurements) > 0:
                raise UserError(_(
                    "You can not segment because order %s has exceptions") % (
                    procurement.group_id.name))
        return super(MrpSegmentLine, self).create(vals)

    @api.multi
    def unlink(self):
        for line in self:
            if line.segment_id.state in ('confirm', 'done'):
                raise UserError(_("Can only be removed in the \
                    construction state of the segment"))
        return super(MrpSegmentLine, self).unlink()
