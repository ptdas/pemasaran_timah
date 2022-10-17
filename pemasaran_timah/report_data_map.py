# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

# mappings for table dumps
# "remember to add indexes!"

data_map = {
    "Sales Invoice[Sales Analytics with Currency]": {
		"columns": ["name", "customer", "posting_date", "currency", "company"],
		"conditions": ["docstatus=1"],
		"order_by": "posting_date",
		"links": {
			"customer": ["Customer", "name"],
			"company":["Company", "name"]
		}
	},
    "Sales Invoice Item[Sales Analytics with Currency]": {
		"columns": ["name", "parent", "item_code", "stock_qty as qty", "base_net_amount", "net_amount"],
		"conditions": ["docstatus=1", "ifnull(parent, '')!=''"],
		"order_by": "parent",
		"links": {
			"parent": ["Sales Invoice", "name"],
			"item_code": ["Item", "name"]
		}
	},
    "Sales Order[Sales Analytics with Currency]": {
		"columns": ["name", "customer", "transaction_date as posting_date", "currency", "company"],
		"conditions": ["docstatus=1"],
		"order_by": "transaction_date",
		"links": {
			"customer": ["Customer", "name"],
			"company":["Company", "name"]
		}
	},
    "Sales Order Item[Sales Analytics with Currency]": {
		"columns": ["name", "parent", "item_code", "stock_qty as qty", "base_net_amount", "net_amount"],
		"conditions": ["docstatus=1", "ifnull(parent, '')!=''"],
		"order_by": "parent",
		"links": {
			"parent": ["Sales Order", "name"],
			"item_code": ["Item", "name"]
		}
	},
    "Delivery Note[Sales Analytics with Currency]": {
		"columns": ["name", "customer", "posting_date", "currency", "company"],
		"conditions": ["docstatus=1"],
		"order_by": "posting_date",
		"links": {
			"customer": ["Customer", "name"],
			"company":["Company", "name"]
		}
	},
    "Delivery Note Item[Sales Analytics with Currency]": {
		"columns": ["name", "parent", "item_code", "stock_qty as qty", "base_net_amount", "net_amount"],
		"conditions": ["docstatus=1", "ifnull(parent, '')!=''"],
		"order_by": "parent",
		"links": {
			"parent": ["Delivery Note", "name"],
			"item_code": ["Item", "name"]
		}
	}
}