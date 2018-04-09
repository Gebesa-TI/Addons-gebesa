# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError
from openerp.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    notify_approval = fields.Char(
        string=_(u'Notify approval'),
        size=100,
    )

    date_delivery = fields.Date(
        string=_(u'Date delivery'),
        default=fields.Date.today,
    )

    date_reception = fields.Date(
        string=_(u'Date reception'),
        default=fields.Date.today,
    )

    total_net_sale = fields.Float(
        string=_(u'Total net sale'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    perc_freight = fields.Float(
        string=_(u'Freight percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_freight = fields.Float(
        string=_(u'Total Freight'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    perc_installation = fields.Float(
        string=_(u'installation percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_installation = fields.Float(
        string=_(u'Total installation'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    profit_margin = fields.Float(
        string=_(u'Profit margin'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    not_be_billed = fields.Boolean(
        string=_(u'not be billed'),
    )

    manufacture = fields.Selection(
        [('special', _(u'Special')),
            ('line', _(u'Line')),
            ('replenishment', _(u'Replenishment')),
            ('semi_special', _(u'Semi special'))],
        string=_(u"Manufacture"),
    )

    executive = fields.Char(
        string=_(u'Executive'),
        size=100,
    )

    respo_reple = fields.Char(
        string=_(u'Responsible of replenishment'),
        size=200,
    )

    priority = fields.Selection(
        [('high', _(u'High')), ('replenishment', _(u'Replenishment')),
         ('express', _(u'Express')), ('sample', _(u'Sample'))],
        _(u'Manufacturing priority'),)

    complement_saleorder_id = fields.Many2one(
        'sale.order',
        string=_(u'In complement:'),
        help=_(u'Displays a list of sales orders'),
    )

    manufacturing_observations = fields.Text(
        string=_(u'Observations Manufacturing'),
    )

    replenishing_motif = fields.Text(
        string=_(u'Reason for the replenishment'),
    )

    credit_status = fields.Selection(
        [('normal', _(u'Normal')),
         ('suspended', _(u'Suspended for Collection')),
         ('conditioned', _(u'Conditioned'))],
        _(u'Credit status'),)

    credit_note = fields.Text(
        string=_(u'Note Credit and Collections'),
    )

    date_production = fields.Date(
        string=_('Date of Production Termination'),
    )

    approve = fields.Selection(
        [('approved', _('Approved')),
         ('suggested', _('Suggested for Approval')),
         ('not_approved', _('Not Approved'))],
        default='not_approved',
        string=_('Approve Status'),
        store=True,
        copy=False,
    )

    total_cost = fields.Float(
        string=_('Total cost'),
        compute='_compute_profit_margin',
        store=True
    )

    sale_picking_adm = fields.Boolean(
        string=_(u'Admin Sale Picking'),
    )

    webiste_operator = fields.Boolean(
        string=_('Captured by Operator'),
    )

    date_suggested = fields.Datetime(
        string=_('Suggestion Date Approval'),
        copy=False,
        help=_('Suggestion Date Approval.'))

    date_approved = fields.Datetime(
        string=_('Credit Release Date'),
        copy=False,
        help=_('Credit Release Date.'))

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The order name must be unique"),
    ]

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.webiste_operator = False
        self.notify_approval = False
        if self.partner_id:
            self.webiste_operator = True
        if self.partner_id.notify_approval:
            self.notify_approval = self.partner_id.notify_approval

    @api.depends('order_line.net_sale')
    def _compute_profit_margin(self):
        for order in self:
            global_cost = 0.0
            global_net_sale = 0.0
            global_freight = 0.0
            global_installa = 0.0
            global_profit_margin = 0.0
            currency = order.company_id.currency_id
            for line in order.order_line:
                global_cost += line.standard_cost
                global_net_sale += line.net_sale
                global_freight += line.freight_amount
                global_installa += line.installation_amount
            if global_net_sale > 0.000000:
                global_total_pm = currency.compute(
                    global_cost, order.pricelist_id.currency_id)
                global_profit_margin = (
                    1 - (global_total_pm) / global_net_sale)
                global_profit_margin = global_profit_margin * 100

            order.total_cost = global_cost
            order.total_net_sale = global_net_sale
            order.total_freight = global_freight
            order.total_installation = global_installa
            order.profit_margin = global_profit_margin

    @api.multi
    @api.onchange('project_id')
    def onchange_project_id(self):
        """
        Trigger the change of warehouse when the analytic account is modified.
        """
        if self.project_id and self.project_id.warehouse_id:
            self.warehouse_id = self.project_id.warehouse_id
        return {}

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.company_id.is_manufacturer:
                order.validate_manufacturing()
                if not order.notify_approval:
                    raise UserError(
                        _('The following field is not invalid:\nNotify approval'))
                if not order.manufacture:
                    raise UserError(
                        _('The following field is not invalid:\nManufacture'))
                # if not order.executive:
                #     raise UserError(
                #         _('The following field is not invalid:\nExecutive'))
                if not order.priority:
                    raise UserError(
                        _('The following field is not invalid:\nManufacturing \
                          priority'))
                if not order.project_id:
                    raise UserError(
                        _('The following field is not invalid:\nAnalytic Account'))
                if not order.client_order_ref:
                    raise UserError(_('This Sale Order not has OC captured'))
                # Comented toda vez que ya hay un modulo de 
                # PLM que considera productos cotizacion:
                # for line in order.order_line:
                #     if line.product_id.quotation_product:
                #         raise UserError(_('The Product contains Quotation'))

        return super(SaleOrder, self).action_confirm()

    @api.multi
    def validate_manufacturing(self):
        for order in self:

            # pending = self.env['sale.order'].search(
            # [('state', '=', 'draft')])
            # dife = 0.0
            # dife = order.amount_total - order.total_nste
            # if order.total_nste > 0.0000000:
            #     if abs(dife) > 0.6000:
            #         raise UserError(
            #             _('The amount are differents:\nAnalytic Account'))

            for line in order.order_line:
                if line.product_id:
                    routes = line.product_id.route_ids + \
                        line.product_id.categ_id.total_route_ids
                    if line.product_id.type == 'service':
                        continue
                    if len(routes) < 2:
                        raise UserError(
                            _('%s %s %s' % (
                                _("The next product has no a valid Route"),
                                line.product_id.default_code,
                                line.product_id.name)))
                    product_bom = False
                    for bom in line.product_id.product_tmpl_id.bom_ids:
                        if bom.product_id.id == line.product_id.id:
                            product_bom = bom or False
                    if not product_bom:
                        raise UserError(
                            _('%s %s %s' % (
                                _("The next product has no a Bill of Materials"),
                                line.product_id.default_code, line.product_id.name)))

                    # if not line.product_id.product_service_id:
                    #     raise UserError(
                    #         _('%s %s %s' % (
                    #             _("The next product has not a SAT Code: "),
                    #             line.product_id.default_code, line.product_id.name)))

        return True

    @api.multi
    def approve_action(self):
        for order in self:
            if order.approve == 'approved':
                raise UserError(_('This Sale Order is already approved'))
            if order.create_uid.id == order.write_uid.id:
                if order.manufacture != 'replenishment' or \
                   order.priority != 'replenishment':
                    raise UserError(_('Este no es un Pedido de Reposición solicita \
                    la aprobación de Credito y Cobranza.'))
            order.write({'approve': 'approved'})
            order.date_approved = fields.Datetime.now()

        # resws = super(SaleOrder, self)._product_data_validation()

        return True

    @api.multi
    def suggested_action(self):
        for order in self:
            if order.approve == 'suggested':
                raise UserError(_('This Sale Order is already Suggested for Approval'))
            if not order.order_line:
                raise UserError(_('This Sale Order not has Products Captured'))
            if not order.client_order_ref:
                raise UserError(_('This Sale Order not has OC captured'))
            if order.partner_id.parent_id:
                order.partner_id = order.partner_id.parent_id
            order.write({'approve': 'suggested'})
            order.date_suggested = fields.Datetime.now()

            if order.company_id.is_manufacturer:
                resws = order._product_data_validation()
                resws2 = order.product_data_validation2()
        # if resws[0] != 'OK':
        #     raise ValidationError('Este pedido no podra ser aprobado  \
        #         debido a errores de configuracion \
        #         en los productos que ocasionarian \
        #         excepciones, se ha enviado un correo detallado a los \
        #         interesados.')

        return True

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['perc_freight'] = self.perc_freight
        invoice_vals['perc_installation'] = self.perc_installation
        # invoice_vals['executive'] = self.executive
        invoice_vals['manufacture'] = self.manufacture

        return invoice_vals

    @api.multi
    def action_done(self):
        super(SaleOrder, self).action_done()

        # commented temporary til implementatio of CRM
        self.force_quotation_send()

    @api.multi
    def force_quotation_send(self):
        for order in self:
            email_act = order.action_quotation_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                notify = order.notify_approval
                email_ctx.update(default_email_to=notify)
                email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True
