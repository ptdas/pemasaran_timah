# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.model.mapper import get_mapped_doc

class custom_method(Document):
	pass
@frappe.whitelist()
def update_est_date(doc,method):
	if doc.items[0].warehouse:
		warehouse_patokan = doc.items[0].warehouse
		warehouse = frappe.get_doc("Warehouse",warehouse_patokan)
		if warehouse.est_hari:
			if warehouse.est_hari > 0:
				doc.est_arrival_date = warehouse.est_hari
				frappe.db.sql(""" UPDATE `tabDelivery Note` SET est_arrival_date = DATE_ADD(DATE("{0}"), INTERVAL {1} DAY) WHERE name = "{2}" """.format(doc.posting_date,warehouse.est_hari,doc.name))
				frappe.db.commit()



@frappe.whitelist()
def get_batch_sales_order_item(sales_order):
	data = frappe.db.sql(""" SELECT batch_no, parent FROM `tabSales Order Item` WHERE parent = "{}"  """.format(sales_order))
	return data


@frappe.whitelist()
def get_booking_for_sales_order(booking_form):
	data = frappe.db.sql(""" SELECT bbi.item_code, bbi.qty, bbi.warehouse, bbi.no_batch, bbi.parent, ti.item_name, ti.description, ti.stock_uom FROM `tabBooking Batch Item` bbi JOIN `tabItem` ti ON ti.item_code = bbi.item_code WHERE bbi.parent = "{}" """.format(booking_form))
	return data

@frappe.whitelist()
def check_booking_booking_form(doc, method):
	for row in doc.batch_list:
		data = frappe.db.sql(""" 
				SELECT 
				a.qty -b.qty , b.name, b.qty, a.qty
				FROM 
				( 
				SELECT sle.`item_code`, sle.`warehouse`, SUM(sle.`actual_qty`) as qty , sle.`batch_no`
				FROM `tabStock Ledger Entry` sle

				WHERE
				sle.`batch_no` = "{0}" AND
				sle.`item_code` = "{1}" AND 
				sle.warehouse = "{2}" AND sle.`docstatus` = 1

				GROUP BY sle.`batch_no`,sle.`item_code`,sle.`warehouse` 
				) a


				LEFT JOIN (
				SELECT SUM(bbi.`qty`) AS qty , bbi.`no_batch`, bbi.`item_code`, bbi.`warehouse`, GROUP_CONCAT(bb.name) as `name`
				FROM `tabBooking Batch Item` bbi 
				JOIn `tabBooking Form` bb ON bb.name = bbi.parent 
				WHERE bb.`docstatus` = 1 AND bb.`booking_status` = "Booked" AND
				bbi.`no_batch` = "{0}" AND
				bbi.`item_code` = "{1}" AND 
				bbi.warehouse = "{2}"

				) b ON b.no_batch = a.`batch_no` AND b.item_code = a.`item_code` AND b.warehouse = a.`warehouse`

				""".format(row.no_batch,row.item_code,row.warehouse))
		if data:
			if data[0]:
				if data[0][0] or data[0][0] == 0:
					if data[0][0] < row.qty:
						frappe.throw("Jumlah yang ingin dibooking melebihi sisa qty Item {0} di gudang {1} setelah perhitungan Booking. Mohon di cek kembali (Qty yang tersisa di gudang : {2}, Qty Booking di {3} : {4} ) ".format(row.item_code,row.warehouse,data[0][3],data[0][1],data[0][2]))

@frappe.whitelist()
def check_booking_order_stock(doc, method):
	for row in doc.items:
		if row.s_warehouse:
			data = frappe.db.sql(""" SELECT 
				a.qty -b.qty , b.name, b.qty, a.qty
				FROM 
				( 
				SELECT sle.`item_code`, sle.`warehouse`, SUM(sle.`actual_qty`) as qty , sle.`batch_no`
				FROM `tabStock Ledger Entry` sle

				WHERE
				sle.`batch_no` = "{0}" AND
				sle.`item_code` = "{1}" AND 
				sle.warehouse = "{2}" AND sle.`docstatus` = 1

				GROUP BY sle.`batch_no`,sle.`item_code`,sle.`warehouse` 
				) a


				LEFT JOIN (
				SELECT SUM(bbi.`qty`) AS qty , bbi.`no_batch`, bbi.`item_code`, bbi.`warehouse`, GROUP_CONCAT(bb.name) as `name`
				FROM `tabBooking Batch Item` bbi 
				JOIn `tabBooking Form` bb ON bb.name = bbi.parent 
				WHERE bb.`docstatus` = 1 AND bb.`booking_status` = "Booked" AND
				bbi.`no_batch` = "{0}" AND
				bbi.`item_code` = "{1}" AND 
				bbi.warehouse = "{2}"

				) b ON b.no_batch = a.`batch_no` AND b.item_code = a.`item_code` AND b.warehouse = a.`warehouse` """.format(row.batch_no,row.item_code,row.s_warehouse))
			if data:
				if data[0]:
					if data[0][0] or data[0][0] == 0:
						if data[0][0] < row.qty:
							frappe.throw("Jumlah yang ingin distockentry melebihi sisa qty Item {0} di gudang {1} setelah perhitungan Booking. Mohon di cek kembali (Qty yang tersisa di gudang : {2}, Qty Booking di {3} : {4} ) ".format(row.item_code,row.s_warehouse,data[0][3],data[0][1],data[0][2]))
	frappe.throw("1")

@frappe.whitelist()
def check_booking_order(doc, method):
	for row in doc.items:
		if row.booking_no:
			cek = frappe.db.sql(""" 
				SELECT bfi.parent
				FROM `tabSales Order Item` bfi 
				WHERE bfi.booking_no = "{0}" AND bfi.parent != "{1}" AND bfi.docstatus = 1 """.format(row.booking_no,doc.name))

			if cek:
				if cek[0]:
					if cek[0][0]:
						frappe.throw("Nomor batch {0} masih terbooking dan dipakai oleh Sales Order {1}".format(row.batch_no,cek[0][0]))
					else:
						frappe.db.sql(""" UPDATE `tabBooking Form` SET sales_order = "{0}" WHERE name = "{1}" """.format(doc.name, row.booking_no))
						frappe.db.commit()
				else:
					frappe.db.sql(""" UPDATE `tabBooking Form` SET sales_order = "{0}" WHERE name = "{1}" """.format(doc.name, row.booking_no))
					frappe.db.commit()
			else:
				frappe.db.sql(""" UPDATE `tabBooking Form` SET sales_order = "{0}" WHERE name = "{1}" """.format(doc.name, row.booking_no))
				frappe.db.commit()

@frappe.whitelist()
def release_booking_order(doc, method):
	for row in doc.items:
		if row.booking_no:
			frappe.db.sql(""" UPDATE `tabBooking Form` SET booking_status = "Released" WHERE name = "{0}" """.format(row.booking_no))
			frappe.db.commit()


@frappe.whitelist()
def reminder_booking():
	data = frappe.db.sql(""" 
		SELECT CONCAT("Reminder Untuk Booking Form ",GROUP_CONCAT(bfi.parent))
		FROM `tabBooking Batch Item` bfi 
		JOIN `tabBooking Form` bf ON bfi.parent = bf.name 
		WHERE bf.booking_status = "Booked" AND bf.docstatus = 1
		AND bf.`reminder` <= CURDATE() AND bf.booking_to_date >= CURDATE() 
		AND bf.owner = "{}" """.format(frappe.session.user))
	if data[0][0]:
		return data
	else:
		return

@frappe.whitelist()
def get_so_from_ta(nomor_ta):
	data = frappe.db.sql(""" 
	SELECT sor.nomor_ta, sor.tanggal_ta, sor.`customer`, soi.brand , SUM(soi.`qty`),AVG(soi.rate),sor.`grand_total`
 	FROM `tabSales Order` sor 
 	JOIN `tabSales Order Item` soi ON soi.parent = sor.name
 	WHERE sor.nomor_ta = "{}" """.format(nomor_ta))
	return data


@frappe.whitelist()
def sync_so_po(doc,method):
	if doc.amended_from and doc.company != "Indometal":
		return
	doc = frappe.get_doc(doc.doctype, doc.name)
	
	pr_doc = frappe.new_doc("Purchase Order")
	pr_doc.doctype = "Purchase Order"
	pr_doc_items = []
	counter = 0
	for row in doc.items:
		pr_doc.append('items')
		pr_doc.items[counter].item_code = row.item_code
		pr_doc.items[counter].qty = row.qty
		pr_doc.items[counter].stock_uom = row.stock_uom
		pr_doc.items[counter].rate = row.rate
		pr_doc.items[counter].price_list_rate = row.price_list_rate
		pr_doc.items[counter].discount_percentage = row.discount_percentage
		pr_doc.items[counter].uom = row.uom
		pr_doc.items[counter].conversion_factor = row.conversion_factor
		pr_doc.items[counter].schedule_date = row.delivery_date
		pr_doc.items[counter].warehouse = row.warehouse.replace("- T", "- I")
		counter = counter + 1

	pr_doc.supplier = "PT TIMAH tbk"
	pr_doc.company = "Indometal"
	pr_doc.naming_series = "PO-In-.#####"
	pr_doc.transaction_date = doc.transaction_date
	pr_doc.sales_order_patokan = doc.name
	pr_doc.save()