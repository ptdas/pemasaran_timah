# -- coding: utf-8 --
# from _future_ import unicode_literals
import frappe
from frappe.utils.background_jobs import enqueue


@frappe.whitelist()
def back_submit(doctype,docname,pilihan):
	doc = frappe.get_doc(doctype,docname)

	if pilihan == 'submit':
		doc.submit()

	if pilihan == "cancel":
		doc.cancel()

@frappe.whitelist()
def enqueue_submit(doctype,docname,pilihan):
	enqueue("pemasaran_timah.backend.back_submit",queue='long', doctype=doctype,docname=docname,pilihan=pilihan)