# Copyright (c) 2013, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = [
		"Date:Data:100",
		"Index Dollar:Currency:200",
		"Harga Timah:Currency:200",
		"Harga Minyak Mentah:Currency:200",

		"Harga Nikel:Currency:200",
		"Harga Alumunium:Currency:200",
		"Nama Metal Lainnya:Data:100",
		"Harga Metal Lainnya:Currency:200",
		]

	data_harga = frappe.db.sql(""" 
		SELECT 
		DATE_FORMAT(tffh.date, "%d-%m-%Y"), 
		tffh.index_dollar, 

		tffh.harga_timah,
		tffh.harga_minyak_mentah, 
		tffh.harga_nikel, 
		tffh.harga_alumunium,

		tc.metal,
		tc.keterangan

		FROM `tabFaktor Fundamental Harian` tffh
		LEFT JOIN `tabTabel Copper` tc ON tc.parent = tffh.name
		WHERE tffh.date BETWEEN "{}" AND "{}"
		ORDER BY tffh.date
	 """.format(filters.get("from_date"), filters.get("to_date")))

	data_rata = frappe.db.sql(""" 
		SELECT 
		AVG(index_dollar), 
		AVG(harga_timah),
		AVG(harga_minyak_mentah), 
		AVG(harga_nikel), 
		AVG(harga_alumunium),
		AVG(tc.keterangan)

		FROM `tabFaktor Fundamental Harian` tffh
		LEFT JOIN `tabTabel Copper` tc ON tc.parent = tffh.name
		WHERE tffh.date BETWEEN "{}" AND "{}"
		ORDER BY date
	 """.format(filters.get("from_date"), filters.get("to_date")))

	date_table = []
	for row in data_harga:
		if row[0] in date_table:
			data.append(["","","","","","",row[6],row[7]])
		else:
			date_table.append(row[0])
			data.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]])
			

	for row in data_rata:
		data.append(["AVG",row[0],row[1],row[2],row[3],row[4],"",row[5]])
	
	return columns, data
