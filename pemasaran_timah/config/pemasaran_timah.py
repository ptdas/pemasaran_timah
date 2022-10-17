from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Setup"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Bank"
				},
				{
					"type": "doctype",
					"name": "Booking Form"
				},
				{
					"type": "doctype",
					"name": "Daily Price"
				},
				{
					"type": "doctype",
					"name": "Dokumen Authorization Release"
				},
				{
					"type": "doctype",
					"name": "Faktor Fundamental Harian"
				},
				{
					"type": "doctype",
					"name": "Forwarder"
				},
				{
					"type": "doctype",
					"name": "Incoterms"
				},
				{
					"type": "doctype",
					"name": "Invoice Pengapalan"
				},
				{
					"type": "doctype",
					"name": "Invoice Storage"
				},
				{
					"type": "doctype",
					"name": "Kode Pelabuhan"
				},
				{
					"type": "doctype",
					"name": "Letter of Indemnity"
				},
				{
					"type": "doctype",
					"name": "Rute"
				},
				{
					"type": "doctype",
					"name": "Shipping Instruction Bursa"
				},				
                {
					"type": "doctype",
					"name": "Shipping Instruction Forwarder"
				},
				{
					"type": "doctype",
					"name": "Status Pengiriman"
				},
				{
					"type": "doctype",
					"name": "Terms Of Payment"
				},
				{
					"type": "doctype",
					"name": "Port"
				},
				{
					"type": "doctype",
					"name": "Series Timah"
				}
			]
		},
        {
			"label": _("Standart Report"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "report",
                    "is_query_report": True,
					"name": "Faktor Fundamental Bulanan",
					"label": _("Faktor Fundamental Bulanan")
				},{
					"type": "report",
                    "is_query_report": True,
					"name": "Report Daily Price",
					"label": _("Report Daily Price")
				},{
					"type": "report",
                    "is_query_report": True,
					"name": "Stock Balance dan Booking",
					"label": _("Stock Balance dan Booking")
				}
			]
		},
        {
			"label": _("Analytics"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "page",
					"name": "sales-analytics-curr-1",
					"label": _("Sales Analytics with Currency"),
				}
			]
		}
    ]
