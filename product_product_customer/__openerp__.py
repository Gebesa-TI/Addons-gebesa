# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Customer product code",
    "summary": "Customer product code",
    "version": "9.0.1.0.0",
    "category": "Inventory",
    "website": "https://odoo-community.org/",
    "author": "<Samuel Barron>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "product",
        "sale",
    ],
    "data": [
        "views/product_product_customer.xml",
        "security/ir.model.access.csv"
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
