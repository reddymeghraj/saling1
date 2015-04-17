# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	client_credit = get_credit(filters)
	data = []
	for d in client_credit:
		row = [d.client_name,d.client_mobile,d.client_email,d.remaining_amount]
		data.append(row)
	return columns, data
def get_columns():
	return [("Client Name")+"::150",("Client mobile")+"::150",("Client Email")+"::200",("Amount")+"::100"]
def get_credit(filters):
	con=filters.get("client_mobile")
	return frappe.db.sql("""select client_name,client_mobile,client_email,remaining_amount from `tabClient Details` where remaining_amount>0.00""",as_dict=1)