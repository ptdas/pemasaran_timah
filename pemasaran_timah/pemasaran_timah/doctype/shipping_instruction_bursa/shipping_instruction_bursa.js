// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shipping Instruction Bursa', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.custom_consignee = function(doc){
	if(doc.consignee){
		frappe.call({
			method:"pemasaran_timah.pemasaran_timah.doctype.shipping_instruction_bursa.shipping_instruction_bursa.get_customer_address_display",
			args: {
				"customer": doc.consignee
			},
			callback: function(r) {
				if(r.message){
					doc.alamat_consignee = r.message[0][0]
					refresh_field("alamat_consignee")
					doc.address_consignee = r.message[0][1]
					refresh_field("address_consignee")
				}
			}
		})
	}
}

cur_frm.cscript.custom_notify_party = function(doc){
	if(doc.notify_party){
		fetch_np = doc.notify_party
		if (fetch_np == "SAME AS CONSIGNEE"){
			fetch_np = doc.consignee
		}
		frappe.call({
			method:"pemasaran_timah.pemasaran_timah.doctype.shipping_instruction_bursa.shipping_instruction_bursa.get_customer_address_display",
			args: {
				"customer": fetch_np
			},
			callback: function(r) {
				if(r.message){
					doc.alamat_notify_party = r.message[0][0]
					refresh_field("alamat_notify_party")
					doc.address_notify_party = r.message[0][1]
					refresh_field("address_notify_party")
				}
			}
		})
	}
}
