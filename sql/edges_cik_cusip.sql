
select concat(i.accession_number,'-',i.infotable_sk) as "id",
	   s.cik as "start_id",
	   concat(s.cik ,'-', s.periodofreport, '-',  i.cusip , '-', s.filing_date)  as "end_id",
	   'held' as "Type",
	   to_char(to_date(s.filing_date,'DD-MON-YYYY'),'yyyy-MM-dd') as "filing_date:DateTime",
       to_char(to_date(s.periodofreport,'DD-MON-YYYY'),'yyyy-MM-dd') as "period_date:DateTime"
  from public.sec_13f_submission s,
  	   public.sec_13f_infotable i
where s.accession_number = i.accession_number
  and s.filing_date = %s