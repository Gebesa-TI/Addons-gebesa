# -*- coding: utf-8 -*-
# © 2017 Cesar Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order by Procurement's Origin",
    "summary": "This module avoids odoo groups diferent proc's origins in PO",
    "version": "9.0.1.0.0",
    "category": "Custom",
    "website": "https://odoo-community.org/",
    "author": "Cesar Barron, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "purchase",
        "stock",
        "mrp",
        "res_company_manufacturer",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "views/procurement_order.xml",
    ],
    "demo": [
        # "demo/res_partner_demo.xml",
    ],
    "qweb": [
        # "static/src/xml/module_name.xml",
    ]
}
