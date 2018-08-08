# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.exceptions import UserError
from openerp.addons import decimal_precision as dp


class MrpShipment(models.Model):
    _name = 'mrp.shipment'
    _description = 'Shipment'
    _rec_name = 'folio'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    state = fields.Selection(
        [('draft', 'Draft'),
         ('cancel', 'Cancelled'),
         ('confirm', 'In Progress'),
         ('done', 'Validated'),
         ('finished', 'Finished')],
        string=_(u'Status'),
        readonly=True,
        select=True,
        default='draft',
        copy=False
    )
    folio = fields.Char(
        string='Folio',
        required=True,
        readonly=True,
        copy=False,
        default='new',
    )
    reference = fields.Text(
        string=_(u'Reference'),
        required=True,
    )
    date = fields.Date(
        string=_(u'Date of shipment'),
        default=fields.Date.today
    )
    departure_date = fields.Date(
        string=_(u'Departure date'),
        default=fields.Date.today
    )
    meters = fields.Float(
        string=_(u'Meters'),
        compute='_compute_meters'
    )
    freight = fields.Float(
        string=_(u'Freight'),
        compute='_compute_meters',
        digits_compute=dp.get_precision('Account'),
    )
    weight = fields.Float(
        string=_('Weight'),
        compute='_compute_meters',
    )
    amount = fields.Float(
        string=_(u'Amount'),
        compute='_compute_meters',
        digits_compute=dp.get_precision('Account'),
    )
    line_ids = fields.One2many(
        'mrp.shipment.line',
        'shipment_id',
        string=_(u'Shipment Products'),
        readonly=False,
        states={'done': [('readonly', True)]},
        help="Shipment Lines.",
        copy=True
    )
    sale_ids = fields.One2many(
        'mrp.shipment.sale',
        'shipment_id',
        string=_(u'Shipment Order'),
        readonly=False,
        states={'done': [('readonly', True)]},
        copy=True
    )

    @api.depends('line_ids', 'line_ids.quantity_shipped')
    def _compute_meters(self):
        for shipment in self:
            meters = 0
            freight = 0
            amount = 0
            weigh = 0
            for line in shipment.line_ids:
                meters += (line.product_id.volume * line.quantity_shipped)
                freight += (line.order_line_id.freight_amount /
                            line.order_line_id.product_uom_qty) * \
                    line.quantity_shipped
                amount += (line.order_line_id.net_sale /
                           line.order_line_id.product_uom_qty) * \
                    line.quantity_shipped
                weigh += (line.product_id.weight * line.quantity_shipped)
            shipment.meters = meters
            shipment.freight = freight
            shipment.amount = amount
            shipment.weight = weigh

    @api.model
    def create(self, vals):
        if vals.get('folio', 'new') == 'new':
            vals['folio'] = self.env['ir.sequence'].next_by_code(
                'mrp.shipment') or '/'
        return super(MrpShipment, self).create(vals)

    @api.multi
    def unlink(self):
        for shipment in self:
            if shipment.state != 'cancel':
                raise ValidationError(_("You can only delete canceled \
                    shipments"))
        return super(MrpShipment, self).unlink()

    @api.multi
    def prepare_shipment(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def done(self):
        ship_line_obj = self.env['mrp.shipment.line']
        ship_sale_obj = self.env['mrp.shipment.sale']
        concat = ''
        concatenate = ''
        ordenes = []
        add = []
        for ship in self:
            concat += ship.folio + ';' + ship.reference + ';' +\
                ship.date + ';' + ship.departure_date + ';' +\
                str(ship.meters) + ';' + str(ship.freight) + ';' +\
                str(ship.amount)
            for line in ship.line_ids:
                sale_order_id = line.sale_order_id
                self._cr.execute("""SELECT so.name
                                    FROM pedidos_vinculados_sale_order_rel as pvs
                                    JOIN pedidos_vinculados_sale_order_rel as pvs2 on(pvs2.pedidos_vinculados_id = pvs.pedidos_vinculados_id)
                                    JOIN sale_order so ON so.id = pvs2.sale_order_id
                                    LEFT JOIN pedidos_vinculados as pv ON (pv.id = pvs.pedidos_vinculados_id)
                                    WHERE pv.activo = true AND pvs.sale_order_id = %s""", ([sale_order_id.id]))
                if self._cr.rowcount:
                    resultado = self._cr.fetchall()
                    for x in resultado:
                        for i in x:
                            if i not in add:
                                add.append(i)
                if line.quantity_shipped == 0:
                    line.unlink()
                    ship_line = ship_line_obj.search([
                        ('sale_order_id', '=', sale_order_id.id),
                        ('shipment_id', '=', ship.id)])
                    if not ship_line:
                        ship_sale = ship_sale_obj.search([
                            ('sale_id', '=', sale_order_id.id),
                            ('shipment_id', '=', ship.id)])
                        if ship_sale:
                            ship_sale.unlink()
                else:
                    volume = line.quantity_shipped * line.product_id.volume
                    weight = line.quantity_shipped * line.product_id.weight
                    if not line.city:
                        raise UserError(
                            _('The lines of order %s have no city.') % (
                                sale_order_id.name))
                    if not line.street:
                        raise UserError(
                            _('The lines of order %s have no street.') % (
                                sale_order_id.name))
                    if not line.state_id.name:
                        raise UserError(
                            _('The lines of order %s have no state.') % (
                                sale_order_id.name))
                    if not line.country_id.name:
                        raise UserError(
                            _('The lines of order %s have no country.') % (
                                sale_order_id.name))
                    if not line.partner_id.name:
                        raise UserError(
                            _('The lines of order %s have no partner.') % (
                                sale_order_id.name))
                    concatenate += line.partner_id.name + ';' +\
                        line.country_id.name + ';' + line.state_id.name +\
                        ';' + line.city + ';' + line.street + ' '
                    if line.street2:
                        concatenate += line.street2
                    concatenate += ';' + line.sale_order_id.name + ';' +\
                        line.sale_order_id.warehouse_id.name + ';' +\
                        line.sale_order_id.warehouse_id.code + ';' +\
                        str(line.sale_order_id.perc_freight) + ';' +\
                        line.product_code + ';' + line.product_name + ';' +\
                        str(volume) + ';' + str(weight) + ';' +\
                        str(line.quantity_shipped) + ';' +\
                        str(line.standard_cost) + ';' +\
                        str(line.price_unit) + '|'
                for a in ship.line_ids:
                    new = a.sale_order_id.name
                    if not new in ordenes:
                        ordenes.append(new)
            if add:
                for op in add:
                    if not op in ordenes:
                        raise UserError(
                            _('You need to add the Order %s, due is Linked to another order present in this shipment') % (op))
            ship.state = 'done'
        return concat, concatenate

    @api.multi
    def cancel(self):
        for ship in self:
            for line in ship.line_ids:
                line.quantity_shipped = 0
                line.order_line_id._quantity_shipped()
            ship.state = 'cancel'
        return True

    @api.multi
    def finished(self):
        shipment_line_obj = self.env['mrp.shipment.line']
        for ship in self:
            for line in ship.line_ids:
                sale_line = line.order_line_id
                shipment_line = shipment_line_obj.search(
                    [('order_line_id', '=', sale_line.id),
                     ('id', '!=', line.id)])
                qty_shipment = 0
                for ship_line in shipment_line:
                    qty_shipment += ship_line.quantity_shipped
                qty_invoiced = sale_line.qty_invoiced - qty_shipment
                if line.quantity_shipped > qty_invoiced:
                    if qty_invoiced < 0:
                        line.quantity_shipped = 0
                    else:
                        line.quantity_shipped = qty_invoiced
            ship.state = 'finished'
        return True

    @api.multi
    def add(self):
        return {
            'name': 'Add Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.shipment.sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
        }


class MrpShipmentSale(models.Model):
    _name = 'mrp.shipment.sale'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
    )
    shipment_id = fields.Many2one(
        'mrp.shipment',
        string=_(u'Shipment'),
        ondelete='cascade',
        select=True)
    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
    )
    country_id = fields.Many2one(
        'res.country',
        string=_(u'Country'),
    )
    state_id = fields.Many2one(
        'res.country.state',
        string=_(u'State'),
    )
    city = fields.Char(
        string=_(u'City'),
    )
    line_ids = fields.One2many(
        'mrp.shipment.line',
        'shipment_sale_id',
        string=_(u'Shipment Line'),
        readonly=False,
        copy=True
    )

    sale_line_id = fields.Many2one(
        'sale.order.line',
        string=_('Line'),
    )
    volume = fields.Float(
        string=_('Volume'),
        compute='_compute_volume_shipped',
    )

    weight = fields.Float(
        string=_('Weight'),
        compute='_compute_weight_shipped',
    )

    def _compute_volume_shipped(self):
        volum = 0.0
        for line in self:
            for order in line.sale_id:
                self._cr.execute("""SELECT sum(pp.volume * msl.quantity_shipped)
                                    FROM mrp_shipment_line as msl
                                    JOIN sale_order as so ON so.id = msl.sale_order_id
                                    JOIN product_product as pp ON (pp.id = msl.product_id)
                                    WHERE msl.shipment_sale_id =  %s""", ([line.id]))
                if self._cr.rowcount:
                    volum = self._cr.fetchone()[0]
            line.volume = volum

    # @api.depends('sale_line_id')
    def _compute_weight_shipped(self):
        weigh = 0
        for linee in self:
            for order in linee.sale_id:
                self._cr.execute("""SELECT sum(pp.weight * msl.quantity_shipped)
                                    FROM mrp_shipment_line as msl
                                    JOIN sale_order as so ON so.id = msl.sale_order_id
                                    JOIN product_product as pp ON (pp.id = msl.product_id)
                                    WHERE msl.shipment_sale_id =  %s""", ([linee.id]))
                if self._cr.rowcount:
                        weigh = self._cr.fetchone()[0]
            linee.weight = weigh

    @api.multi
    def unlink(self):
        for sale in self:
            for line in sale.line_ids:
                if line.quantity_shipped != 0:
                    raise ValidationError(_("The quantity shipped in a \
                        line is different from 0"))
        return super(MrpShipmentSale, self).unlink()


class MrpShipmentLine(models.Model):
    _name = 'mrp.shipment.line'
    _description = 'Shipment line'

    shipment_id = fields.Many2one(
        'mrp.shipment',
        string=_(u'Shipment'),
        ondelete='cascade',
        select=True
    )
    shipment_sale_id = fields.Many2one(
        'mrp.shipment.sale',
        string=_(u'Shipment Sale'),
        ondelete='cascade',
        select=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
    )
    country_id = fields.Many2one(
        'res.country',
        string=_(u'Country'),
    )
    state_id = fields.Many2one(
        'res.country.state',
        string=_(u'State'),
    )
    city = fields.Char(
        string=_(u'City'),
    )
    street = fields.Char(
        string=_(u'Street'),
    )
    street2 = fields.Char(
        string=_(u'Street2'),
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string=_(u'Sale order'),
    )
    order_line_id = fields.Many2one(
        'sale.order.line',
        string=_(u'Sale order line '),
    )
    quantity = fields.Float(
        string=_(u'Quantity'),
    )
    quantity_shipped = fields.Float(
        string=_(u'Quantity shipped'),
    )
    product_id = fields.Many2one(
        'product.product',
        string=_(u'Product'),
    )
    product_name = fields.Char(
        string=_(u'Name product'),
    )
    product_code = fields.Char(
        string=_(u'Code product'),
    )
    standard_cost = fields.Float(
        string=_(u'Standard cost'),
    )
    price_unit = fields.Float(
        string=_(u'Price Unit'),
    )
    total_price = fields.Float(
        string=_(u'Total price'),
        compute='_compute_total_price'
    )
    total_cost = fields.Float(
        string=_(u'Total cost'),
        compute='_compute_total_cost'
    )

    @api.depends('price_unit', 'quantity_shipped')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.price_unit * line.quantity_shipped

    @api.depends('standard_cost', 'quantity_shipped')
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = line.standard_cost * line.quantity_shipped

    @api.constrains('quantity_shipped')
    def _check_quantity_shipped(self):
        for line in self:
            if line.quantity_shipped > line.quantity:
                raise ValidationError(_("The quantity available is less than \
                                      the quantity shipped"))

    @api.multi
    def unlink(self):
        for line in self:
            if line.quantity_shipped != 0:
                raise ValidationError(_("The quantity shipped in a \
                    line is different from 0"))
        return super(MrpShipmentLine, self).unlink()
