# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Dealer.",
    "summary": "Sale Order Dealer.",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Esther Cisneros, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "sale",
        "mrp",
        "sale",
        "account_invoice_sale_data",
    ],
    "data": [
        'views/sale_order.xml',
        'views/mrp_production.xml',
        'views/res_partner.xml'
    ],
    "demo": [

    ],
    "qweb": [

    ]
}