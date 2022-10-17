// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Storage', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.custom_date_exported = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.date_exported && d.date_receiving){
		d.days = frappe.datetime.get_day_diff(d.date_exported, d.date_receiving)
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.days && d.fee){
		d.sub_total = d.weight_mt * d.days * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.fee){
		d.days_free = d.weight_mt * 14 * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.days_free && d.sub_total){
		d.amount_storage_fee = d.sub_total - d.days_free
		refresh_field("invoice_storage_fee")
	}
}
cur_frm.cscript.custom_date_receiving = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.date_exported && d.date_receiving){
		d.days = frappe.datetime.get_day_diff(d.date_exported, d.date_receiving)
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.days && d.fee){
		d.sub_total = d.weight_mt * d.days * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.fee){
		d.days_free = d.weight_mt * 14 * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.days_free && d.sub_total){
		d.amount_storage_fee = d.sub_total - d.days_free
		refresh_field("invoice_storage_fee")
	}
}

cur_frm.cscript.custom_fee = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.weight_mt && d.days && d.fee){
		d.sub_total = d.weight_mt * d.days * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.fee){
		d.days_free = d.weight_mt * 14 * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.days_free && d.sub_total){
		d.amount_storage_fee = d.sub_total - d.days_free
		refresh_field("invoice_storage_fee")
	}
}

cur_frm.cscript.custom_weight_mt = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.weight_mt && d.days && d.fee){
		d.sub_total = d.weight_mt * d.days * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.weight_mt && d.fee){
		d.days_free = d.weight_mt * 14 * d.fee
		refresh_field("invoice_storage_fee")
	}
	if(d.days_free && d.sub_total){
		d.amount_storage_fee = d.sub_total - d.days_free
		refresh_field("invoice_storage_fee")
	}
}

