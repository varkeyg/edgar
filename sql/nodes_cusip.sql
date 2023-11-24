SELECT upper(i.cusip) as "ID",
	   upper(i.cusip) as "cusip:String",
	   max(upper(i.nameofissuer)) as "issuer:String",
	   max(upper(i.titleofclass)) as "title_of_class:String"
  FROM public.sec_13f_infotable i
group by upper(i.cusip)