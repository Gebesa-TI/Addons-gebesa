# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice - Stock Picking Reference",
    "summary": "Add a field in the invoice referencing to its stock_picking",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Cesar Barron, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "account",
        "stock",
        "res_company_manufacturer"
    ],
    "data": [
        "views/account_invoice_view.xml",
        "security/security.xml"
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
