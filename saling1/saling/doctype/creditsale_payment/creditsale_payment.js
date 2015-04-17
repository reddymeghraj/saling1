cur_frm.cscript.contact_no=function(doc,cdt,cdn)
{
	frappe.call({
		method:"saling1.saling.doctype.creditsale_payment.creditsale_payment.get_info",
		args:{contact:doc.contact_no},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message);
			cur_frm.set_value("client_name",doclist[0]);
			cur_frm.set_value("client_email",doclist[1]);
			cur_frm.set_value("bill_no",doclist[3]);
			cur_frm.set_value("previous_amount",doclist[2]);
		}
	});
}
cur_frm.cscript.paid_amount=function(doc,cdt,cdn)
{
	var ramount=doc.previous_amount-doc.paid_amount;
	cur_frm.set_value("remaining_amount",ramount);
}
cur_frm.cscript.payment_mode=function(doc,cdt,cdn)
{
	var d=doc.payment_mode;
	if(d=='Cash')
	{
		cur_frm.toggle_enable('cheque_no', false);
		cur_frm.toggle_enable('bank', false);
		cur_frm.toggle_enable('bank_name', false);
	}
	else
	{
		cur_frm.toggle_enable('cheque_no', true);
		cur_frm.toggle_enable('bank', true);
		cur_frm.toggle_enable('bank_name', true);
	}
}