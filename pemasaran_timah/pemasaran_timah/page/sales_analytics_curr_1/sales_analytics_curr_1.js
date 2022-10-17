frappe.pages['sales-analytics-curr-1'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Sales Analytics with Currency',
		single_column: true
	});

	new erpnext.SalesAnalyticswithCurrency1(wrapper);

	frappe.breadcrumbs.add("Selling")
}

erpnext.SalesAnalyticswithCurrency1 = frappe.views.TreeGridReport.extend({
	init: function(wrapper) {
		this._super({
			title: __("Sales Analytics with Currency"),
			parent: $(wrapper).find('.layout-main'),
			page: wrapper.page,
			doctypes: ["Item", "Item Group", "Customer", "Company",
				"Fiscal Year", "Sales Invoice[Sales Analytics with Currency]", "Sales Invoice Item[Sales Analytics with Currency]"],
			tree_grid: { show: true }
		});
		this.tree_grids = {
			"Customer": {
				label: __("Customer"),
				show: false,
				item_key: "customer",
				formatter: function(item) {
					return item.customer_name? item.customer_name + " (" + item.name + ")" : item.name;
				}
			}
		}
	},
	make_date_range_columns: function() {
		this.columns = [];

		var me = this;
		var range = this.filter_inputs.range.val();
		this.from_date = frappe.datetime.user_to_str(this.filter_inputs.from_date.val());
		this.to_date = frappe.datetime.user_to_str(this.filter_inputs.to_date.val());
		var date_diff = frappe.datetime.get_diff(this.to_date, this.from_date);

		me.column_map = {};
		me.column_map_idr = {};
		me.last_date = null;

		var add_column = function(date) {
			me.columns.push({
				id: date,
				name: frappe.datetime.str_to_user(date),
				field: date,
				formatter: me.currency_formatter,
				width: 100
			});

			me.columns.push({
				id: date+'_idr',
				name: frappe.datetime.str_to_user(date),
				field: date+'_idr',
				formatter: me.currency_formatter,
				width: 100
			});
		};

		var build_columns = function build_columns(condition) {
			for (var i = 0; i <= date_diff; i++) {
				var date = frappe.datetime.add_days(me.from_date, i);
				if (!condition) condition = function condition() {
					return true;
				};

				if (condition(date)) add_column(date);
				me.last_date = date;

				if (me.columns.length) {
					me.column_map[date] = me.columns[me.columns.length - 2];
					me.column_map_idr[date] = me.columns[me.columns.length - 1];
				}
			}
		};
		
		if (range == 'Daily') {
			build_columns();
		} else if (range == 'Weekly') {
			build_columns(function (date) {
				if (!me.last_date) return true;
				return !(frappe.datetime.get_diff(date, me.from_date) % 7);
			});
		} else if (range == 'Monthly') {
			build_columns(function (date) {
				if (!me.last_date) return true;
				return frappe.datetime.str_to_obj(me.last_date).getMonth() != frappe.datetime.str_to_obj(date).getMonth();
			});
		} else if (range == 'Quarterly') {
			build_columns(function (date) {
				if (!me.last_date) return true;
				return frappe.datetime.str_to_obj(date).getDate() == 1 && in_list([0, 3, 6, 9], frappe.datetime.str_to_obj(date).getMonth());
			});
		} else if (range == 'Yearly') {
			build_columns(function (date) {
				if (!me.last_date) return true;
				return $.map(frappe.report_dump.data['Fiscal Year'], function (v) {
					return date == v.year_start_date ? true : null;
				}).length;
			});
		}

		$.each(this.columns, function (i, col) {
			if(me.columns[i + 2]){
				// console.log(me.columns[i + 1])
				if(me.columns[i + 2].id.length == 10)
				{
					col.name = frappe.datetime.str_to_user(frappe.datetime.add_days(me.columns[i + 2].id, -1));
				}
				else
				{
					col.name = frappe.datetime.str_to_user(frappe.datetime.add_days(me.columns[i + 2].id.slice(0,10), -1))+" IDR";
				}				
			}
			else{
				col.name = frappe.datetime.str_to_user(me.to_date) + (col.id.length  != 10 ? " IDR" : "");
			}
			// col.name = me.columns[i + 1] ? frappe.datetime.str_to_user(frappe.datetime.add_days(me.columns[i + 1].id, -1)) : frappe.datetime.str_to_user(me.to_date);
		});
		// console.log(me.column_map)
	},
	setup_chart: function() {
		this.chart_area.toggle(false);
	},
	setup_columns: function() {
		this.tree_grid = this.tree_grids["Customer"];

		var std_columns = [
			// {id: "check", name: "Plot", field: "check", width: 30,
			// 	formatter: this.check_formatter},
			{id: "name", name: this.tree_grid.label, field: "name", width: 300,
				formatter: this.tree_formatter},
			{id: "total", name: "Total", field: "total", plot: false,
				formatter: this.currency_formatter},
			{id: "total_idr", name: "Total IDR", field: "total_idr", plot: false,
			formatter: this.currency_formatter}
		];

		this.make_date_range_columns();
		this.columns = std_columns.concat(this.columns);
	},
	filters: [
		// {fieldtype:"Select", fieldname: "tree_type", label: __("Tree Type"), options:["Customer"],
		// 	filter: function(val, item, opts, me) {
		// 		return me.apply_zero_filter(val, item, opts, me);
		// 	}},
		// {fieldtype:"Select", fieldname: "based_on", label: __("Based On"), options:["Sales Invoice"]},
		// {fieldtype:"Select", fieldname: "value_or_qty", label:  __("Value"),
		// 	options:[{label: __("Value"), value: "Value"}]},
		{fieldtype:"Date", fieldname: "from_date", label: __("From Date")},
		{fieldtype:"Label", fieldname: "to", label: __("To")},
		{fieldtype:"Date", fieldname: "to_date", label: __("To Date")},
		{fieldtype:"Select", fieldname: "company", label: __("Company"), link:"Company",
			default_value: __("Select Company...")},
		{fieldtype:"Select", label: __("Range"), fieldname: "range",
			options:[{label: __("Daily"), value: "Daily"}, {label: __("Weekly"), value: "Weekly"},
				{label: __("Monthly"), value: "Monthly"}, {label: __("Quarterly"), value: "Quarterly"},
				{label: __("Yearly"), value: "Yearly"}]}
	],
	setup_filters: function() {
		var me = this;
		this._super();

		this.trigger_refresh_on_change(["tree_type", "based_on", "company"]);
	},
	init_filter_values: function() {
		this._super();
		this.filter_inputs.range.val('Monthly');
	},
	prepare_data: function() {		
		var me = this;
		if (!this.tl) {
			// add 'Not Set' Customer & Item
			// (Customer / Item are not mandatory!!)
			frappe.report_dump.data["Customer"].push({
				name: "Not Set",
				parent_customer_group: "All Customer Groups",
				parent_territory: "All Territories",
				id: "Not Set",
			});

			// frappe.report_dump.data["Item"].push({
			// 	name: "Not Set",
			// 	parent_item_group: "All Item Groups",
			// 	id: "Not Set",
			// });
		}
		
		if (!this.tl || !this.tl['Sales Invoice']) {
			this.make_transaction_list('Sales Invoice', "Sales Invoice Item");
		}
		
		var items = frappe.report_dump.data["Customer"];
		
		me.parent_map = {};
		me.item_by_name = {};
		me.data = [];
		$.each(items, function(i, v) {
			var d = copy_dict(v);
			me.data.push(d);
			me.item_by_name[d.name] = d;
			if(d[me.tree_grid.parent_field]) {
				me.parent_map[d.name] = d[me.tree_grid.parent_field];
			}
			me.reset_item_values(d);
		});
		

		this.set_indent();

		this.prepare_balances();
		if(me.tree_grid.show) {
			this.set_totals(false);
			this.update_groups();
		} else {
			this.set_totals(true);
		}

	},
	prepare_balances: function() {
		var me = this;
		var from_date = frappe.datetime.str_to_obj(this.from_date);
		var to_date = frappe.datetime.str_to_obj(this.to_date);

		$.each(this.tl['Sales Invoice'], function(i, tl) {
			if (me.is_default('company') ? true : tl.company === me.company) {
				var posting_date = frappe.datetime.str_to_obj(tl.posting_date);
				if (posting_date >= from_date && posting_date <= to_date) {
					var item = me.item_by_name[tl[me.tree_grid.item_key]] ||
						me.item_by_name['Not Set'];
					if(item){
						// console.log(item);
						item[me.column_map[tl.posting_date].field] += tl.base_net_amount;
						item[me.column_map_idr[tl.posting_date].field] += tl.currency == 'IDR' ? tl.net_amount : 0;
						// (is_idr ? (tl.currency == 'IDR' ? tl.net_amount : 0) : tl.base_net_amount);
					}
				}
			}
		});
		
	},
	// update_groups: function() {
	// 	var me = this;

	// 	$.each(this.data, function(i, item) {
	// 		var parent = me.parent_map[item.name];
	// 		while(parent) {
	// 			var parent_group = me.item_by_name[parent];

	// 			$.each(me.columns, function(c, col) {
	// 				if (col.formatter == me.currency_formatter) {
	// 					parent_group[col.field] =
	// 						flt(parent_group[col.field])
	// 						+ flt(item[col.field]);
	// 				}
	// 			});
	// 			parent = me.parent_map[parent];
	// 		}
	// 	});
	// },
	set_totals: function(sort) {
		var me = this;
		var checked = false;
		$.each(this.data, function(i, d) {
			d.total = 0.0;
			d.total_idr = 0.0;
			$.each(me.columns, function(i, col) {				
				if(col.formatter==me.currency_formatter && !col.hidden && col.field!="total" && col.field!="total_idr"){
					// console.log(col.field);
					if(col.field.length == 10)
					{
						d.total += d[col.field];
					}
					else
					{
						d.total_idr += d[col.field];
					}					
				}
				if(d.checked) checked = true;
			})
		});
		this.data = this.data.filter((d) => { return d.total > 0 || d.total_idr > 0  })
		if(sort)this.data = this.data.sort(function(a, b) { return a.total < b.total; });
	}
});
