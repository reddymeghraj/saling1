cur_frm.cscript.contact_no=function(doc,cdt,cdn)
{
	frappe.call({
		method:"saling1.saling.doctype.credit_sale.credit_sale.get_info",
		args:{contact:doc.contact_no},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message);
			cur_frm.set_value("client_name",doclist[0]);
			cur_frm.set_value("client_email",doclist[1]);
			cur_frm.set_value("bill_no",doclist[3]);
			cur_frm.set_value("previous_remaining",doclist[2]);
		}
	});
}
cur_frm.cscript.brand=function(doc,cdt,cdn)
{
	d=locals[cdt][cdn];
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_brand_name",
		args:{brand:d.brand},
		callback:function(r){
			d.brand_name=r.message;
			refresh_field("item_details");
		}
	});
}
cur_frm.cscript.cloth_type=function(doc,cdt,cdn)
{
	d=locals[cdt][cdn];
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_clothtype_name",
		args:{cloth_type:d.cloth_type},
		callback:function(r)
		{
			d.clothtype_name=r.message;
			refresh_field("item_details");
		}
	});
}
cur_frm.cscript.category=function(doc,cdt,cdn)
{
	d=locals[cdt][cdn];
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_category_name",
		args:{category:d.category},
		callback:function(r){
			d.category_name=r.message;
			refresh_field("item_details");
		}
	});
}
cur_frm.cscript.color=function(doc,cdt,cdn)
{
	d=locals[cdt][cdn];
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_color_name",
		args:{color:d.color},
		callback:function(r){
			d.color_name=r.message;
			refresh_field("item_details");
		}
	});
}
cur_frm.cscript.size=function(doc,cdt,cdn)
{
	d=locals[cdt][cdn];
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_size_value",
		args:{size:d.size,brand:d.brand,cloth_type:d.cloth_type,category:d.category,color:d.color},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message);
			d.size_value=doclist[0];
			d.available_quantity=doclist[1];
			d.price=doclist[2];
			refresh_field("item_details");
		}
	});
}
cur_frm.cscript.discount=function(doc,cdt,cdn)
{
	var d=locals[cdt][cdn];
	var d1=d.discount/100;
	disc=d.quantity*d.price*d1;
	var amount=(d.quantity*d.price)-disc;
	d.amount=amount;
	refresh_field("item_details");
}
cur_frm.cscript.date=function(doc,cdt,cdn)
{
	d=doc.item_details;
    var len=d.length;
	var tamount=0;
	for(i=0;i<len;i++)
	{
		tamount=tamount+d[i].amount;
	}
	cur_frm.set_value("total_amount",tamount);
}
cur_frm.cscript.paid_amount=function(doc,cdt,cdn)
{
	var remaining_amount=(doc.total_amount+doc.previous_remaining)-doc.paid_amount;
	cur_frm.set_value("remaining_amount",remaining_amount);
}
cur_frm.cscript.payment_mode=function(doc,cdt,cdn)
{
	var d=doc.payment_mode;
	if(d=='Cash')
	{
		cur_frm.toggle_enable('cheque_no', false);
	}
	else
	{
		cur_frm.toggle_enable('cheque_no', true);
	}
}
cur_frm.cscript.barcode=function(doc,cdt,cdn)
{
	var d=locals[cdt][cdn];
	var bar=d.barcode;
	frappe.call({
		method:"saling1.saling.doctype.sales.sales.get_item_info",
		args:{bar:bar},
		callback:function(r)
		{
			var doclist = frappe.model.sync(r.message);
			d.brand = doclist[0].brand;
			d.brand_name =doclist[0].brand_name;
			d.cloth_type =doclist[0].cloth_type;
			d.clothtype_name =doclist[0].clothtype_name;
			d.category = doclist[0].category;
			d.category_name=doclist[0].category_name;
			d.color=doclist[0].color;
			d.color_name=doclist[0].color_name;
			d.size=doclist[0].size;
			d.size_value=doclist[0].size_value;
			d.price=doclist[0].saling_price;
			refresh_field('item_details');
		}
	});
}