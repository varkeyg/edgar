
select concat(i.accession_number,'-',i.infotable_sk) as "id",
	   s.cik as "start_id",
	   i.cusip as "end_id",
	   'holding' as "Type",
	   value::float as "value:double",
	   i.sshprnamt as "quantity:double",
	   i.sshprnamttype as "shares_or_pro_rated_amount:String",
	   i.putcall as "putcall:String",
       to_char(to_date(s.periodofreport,'DD-MON-YYYY'),'yyyy-MM-dd') as "report_date:DateTime"
  from public.sec_13f_submission s,
  	   public.sec_13f_infotable i
where s.accession_number = i.accession_number