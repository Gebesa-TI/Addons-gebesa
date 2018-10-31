# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Route Family",
    "summary": "Product Route Family",
    "version": "9.0.1.0.0",
    "category": "Account",
    "website": "https://odoo-community.org/",
    "author": "<Esther Cisneros>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "stock",
        "product_structure_gebesa",

    ],
    "data": [
        "views/product_route_family.xml",

    ],
    "demo": [
    ],
    "qweb": [
    ]
}
