# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CreditsalePayment(Document):
	def on_submit(self):
		que=frappe.db.sql("""update `tabClient Details` set remaining_amount=%s where client_mobile=%s and client_name=%s""",(self.remaining_amount,self.contact_no,self.client_name))
		if self.payment_mode=='Cash':
			que=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
			if que:
				n=int(que)+1
				que1=frappe.db.sql("""insert into `tabCash` set name=%s,client_name=%s,contact_no=%s,amount=%s,date=%s,transaction='1',description='Sales Amount'""",(n,self.client_name,self.contact_no,self.paid_amount,self.date))
			else:	
				n=1
				que1=frappe.db.sql("""insert into `tabCash` set name=%s,client_name=%s,contact_no=%s,amount=%s,date=%s,transaction='1',description='Sales Amount'""",(n,self.client_name,self.contact_no,self.paid_amount,self.date))	
		else:
			qu=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Info`""")[0][0]
			if qu:
				n1=int(qu)+1
				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,client_name=%s,contact_no=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='1',description='Sales Amount'""",(n1,self.client_name,self.contact_no,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
			else:
				n1=1
				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,client_name=%s,contact_no=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='1',description='sales Amount'""",(n1,self.client_name,self.contact_no,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))	
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