// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

cur_frm.add_fetch("name1","employee_name","employee_name")
cur_frm.add_fetch("name1","designation","title")

cur_frm.cscript.custom_consignee = function(doc){
	if(doc.consignee){
		frappe.call({
			method:"pemasaran_timah.pemasaran_timah.doctype.shipping_instruction_bursa.shipping_instruction_bursa.get_customer_address_display",
			args: {
				"customer": doc.consignee
			},
			callback: function(r) {
				if(r.message){
					doc.address = r.message[0][0]
					refresh_field("address")
					doc.consignee_address = r.message[0][1]
					refresh_field("consignee_address")
				}
			}
		})
	}
}

frappe.ui.form.on('Letter of Indemnity', {
	refresh: function(frm) {

	}
});
