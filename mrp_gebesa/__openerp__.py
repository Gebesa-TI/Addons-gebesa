# -*- coding: utf-8 -*-
# © <2016> <César Barrón Bautista>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Gebesa MRP",
    "summary": "Modify MRP's default behavior to adapt it to Gebesa",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Cesar Barrón Bautista>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "mrp",
        "mrp_cut_detail",
        "stock_warehouse_analytic_id",
        "sale_order_gebesa",
    ],
    "data": [
        "views/mrp_bom_view.xml",
        "views/sale_order_view.xml",
        "views/procurement_view.xml",
    ],
    "demo": [
        # "demo/res_partner_demo.xml",
    ],
    "qweb": [
        # "static/src/xml/module_name.xml",
    ]
}
