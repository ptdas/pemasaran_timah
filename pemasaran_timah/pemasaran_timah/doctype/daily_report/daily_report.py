# -*- coding: utf-8 -*-
# Copyright (c) 2019, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DailyReport(Document):
	pass

	def autoname(self):
		self.name = "DP"+"/"+self.posting_date.split("-")[2]+"/"+self.posting_date.split("-")[1]+"/"+self.posting_date.split("-")[0]