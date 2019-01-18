# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_shipment.report_shipment'

    @api.multi
    def render_html(self, data=None):
        bom_obj = self.env['mrp.bom']
        report_obj = self.env['report']
        shipment_obj = self.env['mrp.shipment']
        report = report_obj._get_report_from_name(
            'mrp_shipment.report_shipment')
        docs = shipment_obj.browse(self._ids)
        shipment = {}
        kit = {}

        for ship in docs:
            shipment[ship.id] = {}
            for line in ship.line_ids:
                family = line.product_id.family_id.name
                partner = line.partner_id.name
                city = line.city
                if family not in shipment[ship.id].keys():
                    shipment[ship.id][family] = {}
                if partner not in shipment[ship.id][family].keys():
                    shipment[ship.id][family][partner] = {}
                if city not in shipment[ship.id][family][partner].keys():
                    shipment[ship.id][family][partner][city] = []
                shipment[ship.id][family][partner][city].append(line)
                # self._cr.execute("""SELECT geb_invoice_status From sale_order WHERE id = %s""", ([sale.id]))
                self._cr.execute(
                    """
                    WITH RECURSIVE componentes(product_id, code, name, qty, family, not_kit, r) AS (
                        SELECT
                            pp.id,
                            pp.default_code,
                            COALESCE(ir.value, pp.individual_name, ir2.value, pp.name_template, 'Sin definir') as producto,
                            ROUND((mbl.product_qty / mb.product_qty) * 1,6) AS product_qty,
                            pf.name,
                            CASE WHEN mb2.type = 'phantom' THEN FALSE ELSE TRUE END AS not_kit,
                            CAST(ROW_NUMBER () OVER () AS TEXT)
                        FROM mrp_bom AS mb
                        JOIN mrp_bom_line AS mbl ON mb.id = mbl.bom_id
                        JOIN product_product AS pp ON mbl.product_id = pp.id
                        JOIN product_template AS pt ON pp.product_tmpl_id = pt.id
                        LEFT JOIN product_family AS pf ON pt.family_id = pf.id
                        LEFT JOIN ir_translation AS ir ON ir.res_id = pp.id
                            AND ir.lang = 'es_MX' AND ir.name = 'product.product,individual_name'
                        LEFT JOIN ir_translation AS ir2 ON pt.id = ir2.res_id
                            AND ir2.lang = 'es_MX' AND ir2.name = 'product.template,name'
                        LEFT JOIN mrp_bom AS mb2 ON pp.id = mb2.product_id
                        WHERE mb.product_id = %s AND mb.type = 'phantom'
                        UNION SELECT
                            pp.id,
                            pp.default_code,
                            COALESCE(ir.value, pp.individual_name, ir2.value, pp.name_template, 'Sin definir') as producto,
                            ROUND(c.qty * ((mbl.product_qty / mb.product_qty) * 1), 6) AS product_qty,
                            pf.name,
                            CASE WHEN mb2.type = 'phantom' THEN FALSE ELSE TRUE END AS not_kit,
                            CONCAT(c.r, '-', CAST(ROW_NUMBER () OVER () AS TEXT))
                        FROM componentes AS c
                        LEFT JOIN mrp_bom AS mb ON c.product_id = mb.product_id
                        JOIN mrp_bom_line AS mbl ON mb.id = mbl.bom_id
                        JOIN product_product AS pp ON mbl.product_id = pp.id
                        JOIN product_template AS pt ON pp.product_tmpl_id = pt.id
                        LEFT JOIN product_family AS pf ON pt.family_id = pf.id
                        LEFT JOIN ir_translation AS ir ON ir.res_id = pp.id
                            AND ir.lang = 'es_MX' AND ir.name = 'product.product,individual_name'
                        LEFT JOIN ir_translation AS ir2 ON pt.id = ir2.res_id
                            AND ir2.lang = 'es_MX' AND ir2.name = 'product.template,name'
                        JOIN mrp_bom AS mb2 ON pp.id = mb2.product_id
                        WHERE c.not_kit IS false
                    )
                    SELECT product_id, code, name, SUM(qty), family FROM componentes
                    WHERE not_kit GROUP BY product_id, code, name, family""",
                    ([line.product_id.id]))
                if self._cr.rowcount:
                    if line.product_id.id not in kit.keys():
                        kit[line.product_id.id] = self._cr.fetchall()
                # bom = bom_obj.search([('product_id', '=', line.product_id.id),
                #                       ('type', '=', 'phantom')])
                # if bom:
                #     if line.product_id.id not in kit.keys():
                #         kit[line.product_id.id] = bom

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
            'shipment': shipment,
            'kit': kit,
        }
        return report_obj.render('mrp_shipment.report_shipment', docargs)
