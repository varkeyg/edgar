
select s.cik as "ID",
	   s.cik as "cik:string",
	   max(c.filingmanager_name) as "name:String",
	   max(c.filingmanager_street1) as "addr_1:String",
	   max(c.filingmanager_street2) as "addr_2:String",
	   max(c.filingmanager_city) as "city:String",
	   max(c.filingmanager_stateorcountry) as "state_or_country:String",
	   max(c.filingmanager_zipcode) as "zip:String",
	   'Holder' as "Label"
  from public.sec_13f_submission s,
  	   public.sec_13f_coverpage c
where s.accession_number = c.accession_number
group by s.cik


