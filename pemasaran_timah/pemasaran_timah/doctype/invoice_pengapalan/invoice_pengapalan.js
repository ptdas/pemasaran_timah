// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Pengapalan', {
	refresh: function(frm) {

	}
});
cur_frm.cscript.custom_jumlah_kontainer = function(doc){
	if(doc.jumlah_kontainer && doc.freight_usd){
		doc.amount_usd = doc.jumlah_kontainer * doc.freight_usd
		refresh_field("amount_usd")
	}
}
cur_frm.cscript.custom_freight_usd = function(doc){
	if(doc.jumlah_kontainer && doc.freight_usd){
		doc.amount_usd = doc.jumlah_kontainer * doc.freight_usd
		refresh_field("amount_usd")
	}
}
cur_frm.cscript.custom_validate = function(doc){
	if(doc.amount_usd){
		var jumlah_qty = 0 
		for(row in doc.item){
			jumlah_qty = jumlah_qty + doc.item[row].qty
		}
		doc.freight_per_m_t = doc.amount_usd / jumlah_qty
		refresh_field("freight_per_m_t")
	}
}

cur_frm.cscript.custom_biaya = function(doc,cdt,cdn){
	var bar = locals[cdt][cdn]
	if(bar.qty && bar.biaya){
		bar.amount = bar.qty * bar.biaya
		refresh_field("biaya_lain_lain")
	}
}