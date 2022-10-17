# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShippingInstructionForwarder(Document):
	# def autoname(self):
		
	# 	series = "###/Tbk/UM-5020.1/20-S4.5.3"
	# 	check_series = 1

	# 	check = 0
	# 	while check == 0:
	# 		# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
	# 		no_series = str(check_series).zfill(3)
	# 		# ini juga di ganti ### ke yang lain
	# 		n = series.replace("###", no_series)

	# 		patokan = frappe.get_all(self.doctype, filters={'name': n}, fields=['name'])
	# 		if patokan:
	# 			check_series = int(check_series) + 1
	# 		else:
	# 			check = 1

	# 	self.name = n
	# 	return n

	pass