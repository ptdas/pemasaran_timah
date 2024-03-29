# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "pemasaran_timah"
app_title = "Pemasaran Timah"
app_publisher = "DAS"
app_description = "app Pemasaran untuk Timah"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "ptdigitalasiasolusindo.com"
app_license = "MIT"
website_context = {
        "favicon":      "assets/pemasaran_timah/images/fav.png",
        "splash_image": "assets/pemasaran_timah/images/big.png"
}
# Includes in <head>
# ------------------
app_include_css = "/assets/pemasaran_timah/css/pemasaran_timah.min.css"
#app_include_js = "assets/js/produksi_bijih.min.js"
web_include_css = "/assets/pemasaran_timah/css/pemasaran_timah.min.css"
# include js, css files in header of desk.html
# app_include_css = "/assets/pemasaran_timah/css/pemasaran_timah.css"
# app_include_js = "/assets/pemasaran_timah/js/pemasaran_timah.js"

# include js, css files in header of web template
# web_include_css = "/assets/pemasaran_timah/css/pemasaran_timah.css"
# web_include_js = "/assets/pemasaran_timah/js/pemasaran_timah.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "pemasaran_timah.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pemasaran_timah.install.before_install"
# after_install = "pemasaran_timah.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config



# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

standard_queries = {
	"Terms Of Payment": "pemasaran_timah.custom_method.get_terms_of_payment"
}


doc_events = {
	"Sales Order": {
		# "validate": "pemasaran_timah.custom_method.check_booking_order",
		"on_submit": ["pemasaran_timah.custom_method.check_booking_order"],
		"before_cancel": "pemasaran_timah.custom_method.cancel_so"
	},
	"Delivery Note": {
		"validate": "pemasaran_timah.custom_method.check_stock",
		"on_update": "pemasaran_timah.custom_method.update_est_date",
		"on_submit": "pemasaran_timah.custom_method.release_booking_order",
	},
	"Booking Form": {
		"before_submit": "pemasaran_timah.custom_method.check_booking_booking_form",
	},
	"Stock Entry": {
		"validate": "pemasaran_timah.custom_method.check_booking_order_stock",
	},
	"Sales Invoice": {
		"on_submit": "pemasaran_timah.custom_method.sync_sinv_pr",
		"on_cancel": "pemasaran_timah.custom_method.sync_cancel_sinv_pr"
	},
	"Shipping Instruction Forwarder":{
		"autoname": "pemasaran_timah.custom_method.autoname_ship_inst"
	},
	"Letter of Indemnity":{
		"autoname": "pemasaran_timah.custom_method.autoname_loi"
	},
	"Dokumen Authorization Release":{
		"autoname": "pemasaran_timah.custom_method.autoname_dar"
	}
}

dump_report_map = "pemasaran_timah.report_data_map.data_map"

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pemasaran_timah.tasks.all"
# 	],
# 	"daily": [
# 		"pemasaran_timah.tasks.daily"
# 	],
# 	"hourly": [
# 		"pemasaran_timah.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pemasaran_timah.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pemasaran_timah.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pemasaran_timah.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pemasaran_timah.event.get_events"
# }

