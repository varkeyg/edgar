select s.sic_code as id,
	   s.sic_code as "sic:String",
	   s.office as "office:String",
	   s.industry_title as "industry_title:String",
	   'Industry' as label
  from sec_sic s