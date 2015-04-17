# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Sales(Document):
	def validate(self):
		query=frappe.db.sql("""select * from `tabClient Details` where client_mobile=%s and client_name=%s""",(self.contact_no,self.client_name))
		if query:
			pass
		else:
			q4=frappe.db.sql("""select max(name) from `tabClient Details`""")[0][0]
			if q4:
				name=int(q4)+1
				q=frappe.db.sql("""insert into `tabClient Details` set name=%s,client_mobile=%s,client_name=%s,client_email=%s,remaining_amount='0.00'""",(name,self.contact_no,self.client_name,self.client_email))
			else:
				name=1	
				q=frappe.db.sql("""insert into `tabClient Details` set name=%s,client_mobile=%s,client_name=%s,client_email=%s,remaining_amount='0.00'""",(name,self.contact_no,self.client_name,self.client_email))
	def on_submit(self):
		for d in self.get('item_details'):
			query1=frappe.db.sql("""update `tabStock` set quantity=quantity-%s  where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s""",(d.quantity,d.brand,d.cloth_type,d.category,d.color,d.size));
		if self.payment_mode=='Cash':
			que=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
			if que:
				n=int(que)+1
				que1=frappe.db.sql("""insert into `tabCash` set name=%s,client_name=%s,contact_no=%s,amount=%s,date=%s,transaction='1',description='Sales Amount'""",(n,self.client_name,self.contact_no,self.tatal_amount,self.date))
			else:	
				n=1
				que1=frappe.db.sql("""insert into `tabCash` set name=%s,client_name=%s,contact_no=%s,amount=%s,date=%s,transaction='1',description='Sales Amount'""",(n,self.client_name,self.contact_no,self.total_amount,self.date))	
		else:
			qu=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Info`""")[0][0]
			if qu:
				n1=int(qu)+1
				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,client_name=%s,contact_no=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='1',description='Sales Amount'""",(n1,self.client_name,self.contact_no,self.bank,self.bank_name,self.cheque_no,self.total_amount,self.date))
			else:
				n1=1
				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,client_name=%s,contact_no=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='1',description='sales Amount'""",(n1,self.client_name,self.contact_no,self.bank,self.bank_name,self.cheque_no,self.total_amount,self.date))	
@frappe.whitelist()
def get_info(contact):
	query1=frappe.db.sql("""select client_name,client_email from `tabClient Details` where client_mobile=%s""",(contact))
	options=list()
	if query1:
		options.append(query1[0][0])
		options.append(query1[0][1])
	else:
		options.append('')
		options.append('')	
	q2=frappe.db.sql("""select max(bill_no) from `tabSales`""")[0][0]
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
		q=frappe.db.sql("""select saling_price from `tabPdetails` where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s order by name desc""",(brand,cloth_type,category,color,size))	
		options1.append(q[0][0])
	else:
		frappe.throw("Stock is not available")
	return options1	
@frappe.whitelist()
def get_item_info(bar):
	que=frappe.db.sql("""select brand,brand_name,cloth_type,clothtype_name,category,category_name,color,color_name,size,size_value,saling_price from `tabPdetails` where barcode=%s""",(bar),as_dict=1)
	return que