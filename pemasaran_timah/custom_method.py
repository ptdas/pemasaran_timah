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
def autoname_ship_inst(doc, method):
	if doc.naming_series:
		series = doc.naming_series
		query_series = frappe.db.sql(""" SELECT count FROM `tabSeries Timah` WHERE name = "{0}" """.format(series))
		if len(query_series) > 0 :
			check_series = int(query_series[0][0])
			check = 0
			while check == 0:
				no_series = str(check_series).zfill(4)
				n = series.replace("####", no_series)

				patokan = frappe.get_all(doc.doctype, filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					query_series = frappe.db.sql(""" UPDATE `tabSeries Timah` SET count = {1} WHERE name = "{0}" """.format(series,check_series+1))
					check = 1

		doc.name = n

	if doc.amended_from:
		doc.revisi = doc.revisi + 1
	else:
		doc.revisi = 0
		
	doc.ref = doc.name
	return doc.name
@frappe.whitelist()
def submit_ste():
	ste = frappe.get_doc("Stock Entry","STE-00166")
	ste.submit()

@frappe.whitelist()
def autoname_loi(doc, method):
	# if doc.amended_from:
	# 	return
	if doc.naming_series == "###-LOI-2021":
		series = doc.naming_series
		query_series = frappe.db.sql(""" SELECT count FROM `tabSeries Timah` WHERE name = "{0}" """.format(series))
		if len(query_series) > 0 :
			check_series = int(query_series[0][0])
			check = 0
			while check == 0:
				no_series = str(check_series).zfill(3)
				n = series.replace("###", no_series)

				patokan = frappe.get_all(doc.doctype, filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					query_series = frappe.db.sql(""" UPDATE `tabSeries Timah` SET count = {1} WHERE name = "{0}" """.format(series,check_series+1))
					check = 1

		doc.name = n

@frappe.whitelist()
def autoname_dar(doc, method):
	# if doc.amended_from:
	# 	return
	if doc.naming_series == "###-AOL-2021":
		series = doc.naming_series
		query_series = frappe.db.sql(""" SELECT count FROM `tabSeries Timah` WHERE name = "{0}" """.format(series))
		if len(query_series) > 0 :
			check_series = int(query_series[0][0])
			check = 0
			while check == 0:
				no_series = str(check_series).zfill(3)
				n = series.replace("###", no_series)

				patokan = frappe.get_all(doc.doctype, filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					query_series = frappe.db.sql(""" UPDATE `tabSeries Timah` SET count = {1} WHERE name = "{0}" """.format(series,check_series+1))
					check = 1

		doc.name = n

@frappe.whitelist()
def check_stock(doc,method):
	for d in doc.items:
		qty = 0
		for check_qty in doc.items:
			if d.item_code == check_qty.item_code and d.warehouse == check_qty.warehouse and d.batch_no == check_qty.batch_no and d.idx != check_qty.idx:
				frappe.throw(_("Row #{0}: The batch {1} is inputed in another row #{2}. Please select another batch.").format(d.idx, d.batch_no, check_qty.idx))

@frappe.whitelist()
def repair_gl_entry():
	temp_doc = "STE-00065"
	frappe.db.sql(""" UPDATE `tabSingles` SET `value` = 1 WHERE field = "allow_negative_stock" """)
	docu = frappe.get_doc("Stock Entry", temp_doc)
	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(temp_doc))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(temp_doc))
	
	docu.update_stock_ledger()
	docu.make_gl_entries()
	frappe.db.sql(""" UPDATE `tabSingles` SET `value` = 0 WHERE field = "allow_negative_stock" """)

@frappe.whitelist()
def get_pb_number(batch_no):
	data = frappe.db.sql(""" SELECT ste.pb_number
		FROM `tabStock Entry Detail` ste WHERE ste.batch_no = "{0}" 
		AND ste.docstatus = 1 and ste.pb_number IS NOT NULL AND ste.pb_number != "" """.format(batch_no))
	return data

@frappe.whitelist()
def get_warehouse_tujuan(warehouse):
	data = frappe.db.sql(""" SELECT GROUP_CONCAT(tw.name) FROM `tabWarehouse` tw WHERE tw.company = "{0}" AND tw.is_group = 0 """.format(warehouse))
	return data
	
@frappe.whitelist()
def get_goods_dn(delivery_note):
	data = frappe.db.sql(""" SELECT item_name FROM `tabDelivery Note Item` WHERE parent = "{}" GROUP BY item_code """.format(delivery_note))
	return data

@frappe.whitelist()
def get_batch_dn(delivery_note):
	data = frappe.db.sql(""" SELECT batch_no FROM `tabDelivery Note Item` WHERE parent = "{}" GROUP BY batch_no """.format(delivery_note))
	return data

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
def cancel_so(doc,method):
	for row in doc.items:
		if row.booking_no:
			frappe.db.sql(""" UPDATE `tabBooking Form` SET sales_order = "" WHERE docstatus = 1 AND sales_order = "{}" """.format(doc.name))
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
	if doc.amended_from or not doc.company_tujuan:
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
		pr_doc.items[counter].warehouse = frappe.get_doc("Company", doc.company_tujuan).default_inventory_account
		counter = counter + 1

	pr_doc.supplier = "PT TIMAH tbk"
	pr_doc.company = doc.company_tujuan
	if doc.company_tujuan == "Timah Tbk":
		pr_doc.naming_series = "PO-Tbk-.#####"
	elif doc.company_tujuan == "Indometal (London) Ltd.":
		pr_doc.naming_series = "PO-In-.#####"
	else:
		pr_doc.naming_series = "PO-InAP-.#####"

	pr_doc.transaction_date = doc.transaction_date
	pr_doc.sales_order_patokan = doc.name

	pr_doc.save()

@frappe.whitelist()
def sync_sinv_pr(doc,method):
	if not doc.company_tujuan:
		return

	doc = frappe.get_doc(doc.doctype, doc.name)
	
	pr_doc = frappe.new_doc("Purchase Receipt")
	pr_doc.doctype = "Purchase Receipt"
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
		pr_doc.items[counter].warehouse = doc.warehouse_tujuan
		if row.batch_no:
			pr_doc.items[counter].batch_no = row.batch_no
		counter = counter + 1

	pr_doc.supplier = "PT TIMAH tbk"
	pr_doc.company = doc.company_tujuan
	if doc.company_tujuan == "Timah Tbk":
		pr_doc.naming_series = "PREC-Tbk-.#####"
	elif doc.company_tujuan == "Indometal (London) Ltd.":
		pr_doc.naming_series = "PREC-In-.#####"
	else:
		pr_doc.naming_series = "PREC-InAP-.#####"

	pr_doc.posting_date = doc.posting_date
	pr_doc.sales_invoice_patokan = doc.name

	pr_doc.save()
	pr_doc.submit()

@frappe.whitelist()
def sync_cancel_sinv_pr(doc,method):
	ambil_prec = frappe.db.sql(""" SELECT name FROM `tabPurchase Receipt` WHERE sales_invoice_patokan = "{}" AND docstatus = 1 """.format(doc.name))
	for row in ambil_prec:
		prec = frappe.get_doc("Purchase Receipt", row[0])
		prec.cancel()

@frappe.whitelist()
def sync_sinv_pr_tertentu():
	doc = frappe.get_doc("Sales Invoice","INV/LN/TBK/2020/087-1")

	if not doc.company_tujuan:
		return
		
	doc = frappe.get_doc(doc.doctype, doc.name)
	
	pr_doc = frappe.new_doc("Purchase Receipt")
	pr_doc.doctype = "Purchase Receipt"
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
		pr_doc.items[counter].warehouse = doc.warehouse_tujuan
		if row.batch_no:
			pr_doc.items[counter].batch_no = row.batch_no
		counter = counter + 1

	pr_doc.supplier = "PT TIMAH tbk"
	pr_doc.company = doc.company_tujuan
	if doc.company_tujuan == "Timah Tbk":
		pr_doc.naming_series = "PREC-Tbk-.#####"
	elif doc.company_tujuan == "Indometal (London) Ltd.":
		pr_doc.naming_series = "PREC-In-.#####"
	else:
		pr_doc.naming_series = "PREC-InAP-.#####"

	pr_doc.posting_date = doc.posting_date
	pr_doc.sales_invoice_patokan = doc.name

	pr_doc.save()
	pr_doc.submit()
@frappe.whitelist()
def get_customer_details(customer):
	hasil = frappe.db.sql(""" SELECT tc.customer_name, tas.`city`, tas.`address_line1`, tc.`mobile_no`, tc.`email_id`
		FROM `tabDynamic Link` tdl
		JOIN `tabAddress` tas ON tas.name = tdl.`parent`
		JOIN `tabCustomer` tc ON tc.name = tdl.`link_name`

		WHERE tdl.link_name = "{}" AND tdl.parenttype = "Address" AND tdl.link_doctype = "Customer"
		LIMIT 1""".format(customer))

	return hasil

@frappe.whitelist()
def get_terms_of_payment(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(""" SELECT name, credit_days, keterangan FROM `tabTerms Of Payment` """)
