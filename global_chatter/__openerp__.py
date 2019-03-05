# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Global Chatter",
    "summary": "Add the chatter in the view(s) that do not have it.",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "account",
        "mrp",
        "product",
        "sale",
        "stock",
        'message_post_model',
        "mrp_shipment",
        "stock_batch_picking",
        "project",
        "mail",
    ],
    "data": [
        "views/account_payment_view.xml",
        "views/mrp_view.xml",
        "views/stock_view.xml",
        "views/product_view.xml",
        "views/account_account_view.xml",
        "views/account_move.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
