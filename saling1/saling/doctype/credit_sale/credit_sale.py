# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CreditSale(Document):
	def validate(self):
		query=frappe.db.sql("""select * from `tabClient Details` where client_mobile=%s and client_name=%s""",(self.contact_no,self.client_name))
		if query:
			pass
		else:
			q4=frappe.db.sql("""select max(name) from `tabClient Details`""")[0][0]
			if q4:
				name=int(q4)+1
				q=frappe.db.sql("""insert into `tabClient Details` set name=%s,client_mobile=%s,client_name=%s,client_email=%s,remaining_amount=%s""",(name,self.contact_no,self.client_name,self.client_email,self.remaining_amount))
			else:
				name=1	
				q=frappe.db.sql("""insert into `tabClient Details` set name=%s,client_mobile=%s,client_name=%s,client_email=%s,remaining_amount=%s""",(name,self.contact_no,self.client_name,self.client_email,self.remaining_amount))
	def on_submit(self):
		que=frappe.db.sql("""update `tabClient Details` set remaining_amount=%s where client_mobile=%s and client_name=%s""",(self.remaining_amount,self.contact_no,self.client_name))
		for d in self.get('item_details'):
			query1=frappe.db.sql("""update `tabStock` set quantity=quantity-%s  where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s""",(d.quantity,d.brand,d.cloth_type,d.category,d.color,d.size));

@frappe.whitelist()
def get_info(contact):
	query1=frappe.db.sql("""select client_name,client_email,remaining_amount from `tabClient Details` where client_mobile=%s""",(contact))
	options=list()
	if query1:
		options.append(query1[0][0])
		options.append(query1[0][1])
		if query1[0][2]>0:
			options.append(query1[0][2])
		else:
			options.append(0.00)
	else:
		options.append('')
		options.append('')	
		options.append(0.00)
	q2=frappe.db.sql("""select max(bill_no) from `tabCredit Sale`""")[0][0]
	if q2:
		w=int(q2)+1
		options.append(w)
	else:
		q2=1
		options.append(q2)
	return options
@frappe.whitelist()
def get_brand_name(brand):
	query=frappe.db.sql("""select brand_name from `tabAdd Brand` where name=%s""",brand)
	return query[0][0]
@frappe.whitelist()
def get_clothtype_name(cloth_type):
	query=frappe.db.sql("""select cloth_type from `tabAdd Clothtype` where name=%s""",cloth_type)
	return query[0][0]
@frappe.whitelist()
def get_category_name(category):
	query=frappe.db.sql("""select category from `tabAdd Category` where name=%s""",category)
	return query[0][0]
@frappe.whitelist()
def get_color_name(color):
	query=frappe.db.sql("""select color from `tabAdd Color` where name=%s""",color)
	return query[0][0]
@frappe.whitelist()
def get_size_value(size,brand,cloth_type,category,color):
	query=frappe.db.sql("""select size from `tabAdd Size` where name=%s""",size)
	options1=list()
	options1.append(query[0][0])
	q5=frappe.db.sql("""select quantity from `tabStock` where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s """,(brand,cloth_type,category,color,size))
	if q5:
		options1.append(q5[0][0])	
		q=frappe.db.sql("""select saling_price from `tabPdetails` where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s order by name desc""",(brand,cloth_type,category,color,size))[0][0]		
		options1.append(q)
	else:
		frappe.throw("Stock is not available")
	return options1		
@frappe.whitelist()
def get_item_info(bar):
	que=frappe.db.sql("""select brand,brand_name,cloth_type,clothtype_name,category,category_name,color,color_name,size,size_value,saling_price from `tabPdetails` where barcode=%s""",(bar),as_dict=1)
	return que	