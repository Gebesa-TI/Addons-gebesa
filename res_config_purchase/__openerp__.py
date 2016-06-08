# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Purchase-Price Default",
    "summary": "Res settings purchase",
    "version": "9.0.1.0.0",
    "category": "Purchase",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro>, Odoo Community Association (OCA)",
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
    ],
    "data": [
        "views/res_config_view.xml",
        "views/product_view.xml",

    ],
    "demo": [
    ],
    "qweb": [
    ]
}
