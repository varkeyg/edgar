SELECT concat(s.cik ,'-', s.periodofreport, '-',  i.cusip , '-', s.filing_date) as "ID",
	   max(upper(i.cusip)) as "cusip:String",
	   max(upper(i.nameofissuer)) as "issuer:String",
	   max(upper(i.titleofclass)) as "title_of_class:String",
	   max(s.cik) as "cik:String",
	   max(value::float) as "value:double",
	   max(i.sshprnamt) as "quantity:double",
	   max(i.sshprnamttype) as "shares_or_pro_rated_amount:String",
	   max(i.putcall) as "putcall:String",
       max(to_char(to_date(s.periodofreport,'DD-MON-YYYY'),'yyyy-MM-dd')) as "period_date:DateTime",
	   max(to_char(to_date(s.filing_date,'DD-MON-YYYY'),'yyyy-MM-dd')) as "filing_date:DateTime",
	   max('Holding') as "Label"
  from public.sec_13f_submission s,
  	   public.sec_13f_infotable i
where s.accession_number = i.accession_number
  and filing_date = %s
group by concat(s.cik ,'-', s.periodofreport, '-',  i.cusip , '-', s.filing_date)