# Copyright (c) 2013, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
def execute(filters=None):
	columns, data = [], []
	columns = [
		"Date:Data:100",
		"Cash Buy Price:Data:200",
		"Cash Sell Price:Data:200",
		"3 Month Buy:Data:200",
		"3 Month Sell:Data:200",
		"Settlement:Data:200",
		"+/-:Data:100",

		"LME Stock:Data:100",
		"+/- :Data:100",

		"ICDX Price:Currency:200",
		"+/-     :Data:100",	
		"ICDX Qty:Int:100",
		"ICDX-LME Price:Currency:200",

		"KLTM Daily Price:Data:200",
		"+/-  :Data:100",
		"T/O:Data:200",
		"KLTM-LME Price:Data:200",
		
		"JFX Daily Price:Data:200",
		"+/-   :Data:100",
		"T/O :Data:200",
		"JFX-LME Price:Data:200",

		"X_Rate Buy:Data:200",
		"X_Rate Sell:Data:200",
		"X_Rate Mean:Data:200"
		]

	data_daily = frappe.db.sql(""" SELECT 
								DATE_FORMAT(posting_date, "%d-%M-%Y"),
								
								IFNULL(buy_lme_price_case,0),
								IFNULL(sell_lme_price_case,0),
								IFNULL(lme_3_month_buy,0),
								
								IFNULL(lme_3_month_sell,0),
								IFNULL(sell_lme_price_case,0),
								IFNULL(lme_stock,0),

								IFNULL(icdx_price,0),
								IFNULL(qty_icdx,0),
								IFNULL(kltm_price,0) as kltm,
								IFNULL(qty_kltm,0),

								IFNULL(ny_spot_price,0),
								IFNULL(ny_spot,0),

								FORMAT(IFNULL(x_rate_bi_buy,0),2),
								FORMAT(IFNULL(x_rate_bi_sell,0),2),
								FORMAT((IFNULL(x_rate_bi_sell,0) + IFNULL(x_rate_bi_buy,0))/2,2),
								name,
								(kltm_price-sell_lme_price_case) as tes,
								(ny_spot_price-sell_lme_price_case) as tes2
								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								""".format(filters.get("from_date"), filters.get("to_date")))

	min_kltm_price = []
	min_to = []
	max_kltm = []
	max_jfx = []

	
	for i in data_daily:
		if i[9]:
			if i[9] != 0:
				min_kltm_price.append(i[9])
		if i[10]:
			if i[10] != 0:
				min_to.append(i[10])
		if i[17]:
			if i[17] != 0:
				max_kltm.append(i[17])
		if i[18]:
			if i[18] != 0:
				max_jfx.append(i[18])
	if len(min_kltm_price) > 0:
		mkp = min(min_kltm_price)
	else:
		mkp = 0

	if len(min_to) > 0:
		mt = min(min_to)
	else:
		mt = 0

	if len(max_kltm) > 0:
		mk = max(max_kltm)
	else:
		mk = 0

	if len(max_jfx) > 0:
		mj = max(max_jfx)
	else:
		mj = 0
	# frappe.msgprint(str(max_jfx))


		
	count_data_daily = frappe.db.sql(""" SELECT 
								COUNT(name)

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}" and (buy_lme_price_case !=0 OR sell_lme_price_case != 0)
								""".format(filters.get("from_date"), filters.get("to_date")))

	count_data_kltm = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND kltm_price != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_data_ny_spot = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND qty_kltm != 0 """.format(filters.get("from_date"), filters.get("to_date")))

	
	
	data_max = frappe.db.sql(""" SELECT 
								
								max(buy_lme_price_case),
								max(sell_lme_price_case),
								max(lme_3_month_buy),
								
								max(lme_3_month_sell),
								max(sell_lme_price_case),
								max(lme_stock),

								max(icdx_price),
								max(qty_icdx),

								max(kltm_price),
								max(qty_kltm),

								max(kltm_price-sell_lme_price_case),

								max(ny_spot_price),
								max(ny_spot),

								max(ny_spot_price-sell_lme_price_case),

								FORMAT(max(x_rate_bi_buy),2),
								FORMAT(max(x_rate_bi_sell),2),
								FORMAT(max((x_rate_bi_buy+x_rate_bi_sell)/2),2)

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								""".format(filters.get("from_date"), filters.get("to_date")))

	data_max_ny_spot_to_price = frappe.db.sql(""" SELECT 
								MAX(CAST(ny_spot AS DECIMAL))

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND ny_spot IS NOT NULL AND ny_spot > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	for row in data_max:
		data_max_jfx_price_1 = 0
		if data_max_ny_spot_to_price:
			if data_max_ny_spot_to_price[0]:
				if data_max_ny_spot_to_price[0][0]:
					data_max_jfx_price_1 = data_max_ny_spot_to_price[0][0]

		data.append(["""<div style="text-align: center">$ {}</div>""".format("Max"),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[0])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[1])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[2])), 
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[3])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[4])),
			
			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[5])),
			"",
			"",
			"",

			"",
			"",
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[8])),
			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[9])),

			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(mk)),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[11])),
			"",
			"""<div style="text-align: right"> {}</div>""".format(data_max_jfx_price_1),

			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(mj)),
			row[14],
			row[15],
			row[16]])

	data_min = frappe.db.sql(""" SELECT 
								
								min(buy_lme_price_case),
								min(sell_lme_price_case),
								min(lme_3_month_buy),
								
								min(lme_3_month_sell),
								min(sell_lme_price_case),
								min(lme_stock),

								min(icdx_price),
								min(qty_icdx),

								min(kltm_price),
								min(qty_kltm),

								min(kltm_price-sell_lme_price_case),

								min(ny_spot_price),
								min(ny_spot),

								min(ny_spot_price-sell_lme_price_case),

								FORMAT(min(x_rate_bi_buy),2),
								FORMAT(min(x_rate_bi_sell),2),
								FORMAT(min((x_rate_bi_buy+x_rate_bi_sell)/2),2)

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND sell_lme_price_case > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	data_min_ny_spot_to_price = frappe.db.sql(""" SELECT 
								MIN(CAST(ny_spot AS DECIMAL))

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND ny_spot IS NOT NULL AND ny_spot > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	data_x_rate_min_buy = frappe.db.sql(""" SELECT 
								FORMAT(min(x_rate_bi_buy),2)
							
								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND x_rate_bi_buy > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	data_x_rate_min_sell = frappe.db.sql(""" SELECT 
								FORMAT(min(x_rate_bi_sell),2)
							
								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND x_rate_bi_sell > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	data_min_jfx_price = frappe.db.sql(""" SELECT 
								min(ny_spot_price)

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{}" AND "{}"
								AND ny_spot_price IS NOT NULL AND ny_spot_price > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	for row in data_min:
		data_min_jfx_price_1 = 0
		if data_min_jfx_price:
			if data_min_jfx_price[0]:
				if data_min_jfx_price[0][0]:
					data_min_jfx_price_1 = data_min_jfx_price[0][0]

		data_min_jfx_price_2 = 0
		if data_min_ny_spot_to_price:
			if data_min_ny_spot_to_price[0]:
				if data_min_ny_spot_to_price[0][0]:
					data_min_jfx_price_2 = data_min_ny_spot_to_price[0][0]

		data.append(["""<div style="text-align: center">$ {}</div>""".format("Min"),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[0])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[1])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[2])), 
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[3])),

			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[4])),
			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[5])),
			""
			,"",

			"",
			"",
			"", 
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(mkp)),

			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(mt)),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[10])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(data_min_jfx_price_1)),
			"",

			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(frappe.utils.flt(data_min_jfx_price_2))),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[13])),
			data_x_rate_min_buy[0][0],
			data_x_rate_min_sell[0][0],
			(flt(data_x_rate_min_buy[0][0])+flt(data_x_rate_min_sell[0][0]))/2])

	jum_data = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{}" AND "{}" AND x_rate_bi_buy != 0 """.format(filters.get("from_date"), filters.get("to_date")),as_list=1)
	# frappe.msgprint(str(jum_data[0][0])+"jum_data")
	data_avg = frappe.db.sql(""" SELECT 
								
								sum(buy_lme_price_case)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND buy_lme_price_case != 0),
								sum(sell_lme_price_case)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND sell_lme_price_case != 0),
								sum(lme_3_month_buy)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND lme_3_month_buy != 0),
								
								sum(lme_3_month_sell)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND lme_3_month_sell != 0),
								sum(sell_lme_price_case)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND sell_lme_price_case != 0),
								sum(lme_stock)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND lme_stock != 0),
								
								sum(icdx_price)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND icdx_price != 0),
								avg(qty_icdx),
								
								IFNULL(sum(kltm_price)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND kltm_price != 0),0),
								IFNULL(sum(qty_kltm)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND qty_kltm != 0),0),
								

								avg(kltm_price-sell_lme_price_case),

								sum(ny_spot_price)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ny_spot_price != 0),
								sum(ny_spot)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ny_spot != 0),

								avg(ny_spot_price-sell_lme_price_case),

								FORMAT(sum(x_rate_bi_buy)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND x_rate_bi_buy != 0),2),
								FORMAT(sum(x_rate_bi_sell)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND x_rate_bi_sell != 0),2),
								FORMAT(sum((x_rate_bi_buy+x_rate_bi_sell)/2)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND x_rate_bi_buy != 0 AND x_rate_bi_sell !=0),2),
								name
								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{0}" AND "{1}"
								""".format(filters.get("from_date"), filters.get("to_date")))
	
	data_avg_jfx_price = frappe.db.sql(""" SELECT 
								sum(ny_spot_price)/(SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ny_spot_price !=0)

								FROM `tabDaily Price` 
								WHERE posting_date BETWEEN "{0}" AND "{1}"
								AND ny_spot_price IS NOT NULL AND ny_spot_price > 0
								""".format(filters.get("from_date"), filters.get("to_date")))

	for row in data_avg:
		data_avg_jfx_price_1 = 0
		if data_avg_jfx_price:
			if data_avg_jfx_price[0]:
				if data_avg_jfx_price[0][0]:
					data_avg_jfx_price_1 = data_avg_jfx_price[0][0]
		data.append([
			"""<div style="text-align: center">$ {}</div>""".format("Avg"),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[0])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[1])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[2])), 
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[3])),
			
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[4])),
			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(frappe.utils.flt(row[5]))),
			"",
			"",

			"",
			"",
			"", 
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(frappe.utils.flt(row[8]))),
			"",

			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[9])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[10])),
			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(data_avg_jfx_price_1)),
			"",
			"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(frappe.utils.flt(row[12]))),

			"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[13])),
			row[14],
			row[15],
			row[16]
			])

	
	count_data_kltm2 = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND icdx_price != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_data_ny_spot_price = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ny_spot_price != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_ny = frappe.db.sql(""" SELECT COUNT(name) FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ny_spot != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_jvx_lme = frappe.db.sql(""" SELECT COUNT(ny_spot_price-sell_lme_price_case) as tes2 FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND (ny_spot_price-sell_lme_price_case) != 0 """.format(filters.get("from_date"), filters.get("to_date")))

	count_xrb = frappe.db.sql(""" SELECT COUNT(x_rate_bi_buy) as tes2 FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND (x_rate_bi_buy) != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_xrs = frappe.db.sql(""" SELECT COUNT(x_rate_bi_sell) as tes2 FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND (x_rate_bi_sell) != 0 """.format(filters.get("from_date"), filters.get("to_date")))
	count_xrm = frappe.db.sql(""" SELECT COUNT((x_rate_bi_buy+x_rate_bi_sell)/2) as tes2 FROM `tabDaily Price` WHERE posting_date BETWEEN "{0}" AND "{1}" AND ((x_rate_bi_buy+x_rate_bi_sell)/2) != 0 """.format(filters.get("from_date"), filters.get("to_date")))



	data.append([
		"""<div style="text-align: center"> {}</div>""".format("n"),
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),

		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"",
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"",
		"",

		"",
		"",
		"", 
		"""<div style="text-align: center"> {}</div>""".format(count_data_kltm[0][0]),
		"",

		"""<div style="text-align: center"> {}</div>""".format(count_data_ny_spot[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_data_daily[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_data_ny_spot_price[0][0]),
		"",
		"""<div style="text-align: center"> {}</div>""".format(count_ny[0][0]),
		
		"""<div style="text-align: center"> {}</div>""".format(count_jvx_lme[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_xrb[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_xrs[0][0]),
		"""<div style="text-align: center"> {}</div>""".format(count_xrm[0][0]),
		])

	plusminus1 = 0
	plusminus2 = 0
	plusminus3 = 0
	plusminus4 = 0
	plusminus5 = 0 

	data.append([""])

	for row in data_daily:
		if plusminus1 == 0:
			plusminus1 = row[5]

		if plusminus2 == 0:
			plusminus2 = row[6]

		if plusminus3 == 0:
			plusminus3 = row[9]
		
		if plusminus4 == 0:
			plusminus4 = row[11]
		try:
			data.append([
				row[0],
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[1])),
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[2])),
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[3])),
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[4])),
				
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[4])),
				int(row[5])-int(plusminus1),
				"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[6])),
				int(row[6])-int(plusminus2),
				row[7],int(row[7])-int(plusminus5),
				
				row[8],
				int(row[7]) - int(row[5]),
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[9])),
				int(row[9])-int(plusminus3),
				"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(row[10])),
				
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(frappe.utils.flt(row[9]) - int(row[5]))), 
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[11])), 
				int(row[11] - int(plusminus4)), 
				"""<div style="text-align: right"> {}</div>""".format("{:,.0f}".format(frappe.utils.flt(row[12]))), 
				"""<div style="text-align: right">$ {}</div>""".format("{:,.2f}".format(row[11]-row[5])), 
				
				row[13], 
				row[14], 
				row[15]])
		except:
			frappe.throw(str(row[16]))

		plusminus1 = row[5]
		plusminus2 = row[6]
		plusminus3 = row[9]
		plusminus4 = row[11]




	return columns, data
