# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	item_stock = get_stock(filters)
	data = []
	for d in item_stock:
		row = [d.brand_name,d.clothtype_name,d.category_name,d.color_name,d.size_value,d.quantity]
		data.append(row)
	return columns, data
def get_columns():
	return [("Brand Name")+"::150",("Cloth Type")+"::150",("Category")+"::150",("Color")+"::100",("size")+"::100",("Quantity")+"::100"]
def get_stock(filters):
	con=filters.get("brand_name")
	return frappe.db.sql("""select brand_name,clothtype_name,category_name,color_name,size_value,quantity from `tabStock`""",as_dict=1)