# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShippingInstructionBursa(Document):
	pass

@frappe.whitelist()
def get_customer_address_display(customer):
	address = frappe.db.sql(""" 
		SELECT  CONCAT(IFNULL(ta.`address_line1`,""), "\n", IFNULL(ta.`address_line2`,""), "\n", ta.`city`), ta.name
		FROM `tabDynamic Link` dl 
		JOIN `tabAddress` ta ON ta.name = dl.`parent` 
		WHERE 
		dl.link_doctype = "Customer" AND dl.parenttype = "Address"
		AND link_name ="{}" """.format(customer))

	hasil = []
	adress = ""
	link = ""
	if address:
		if address[0]:
			if address[0][0]:
				adress = address[0][0]
				link = address[0][1]
	hasil.append([adress, link])

	return hasil