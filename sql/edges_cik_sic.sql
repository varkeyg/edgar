select concat(cs.cik,cs.sic) as "id",
       cs.cik as "start_id",  
       cs.sic as "end_id",
       'classified' as "type"
  from public.sec_cik_sic cs