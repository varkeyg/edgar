import requests
import sqlite3
from datetime import datetime, timedelta
import math
import xml.etree.ElementTree as ET
import json
import csv

class Edgar:
    def __init__(self, from_date:str, to_date:str) -> None:
        self.base_url = "https://www.sec.gov/Archives/" #edgar/daily-index/" #2023/QTR4/master.20231024.idx"
        self.from_date = datetime.strptime(from_date, "%Y%m%d")
        self.to_date = datetime.strptime(to_date, "%Y%m%d")
        self.date_range:list =[]
        self.index_records = []
        self.con = sqlite3.connect("edgar.db")
        self.headers = {
                    'User-Agent': 'My Inc. noone@gmail.com',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'www.sec.gov'
                   }
        self.data_file = "data.csv"
        self.itable = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
        
    
    def http_get(self, url):
        resp = requests.get(url,headers=self.headers)
        return resp.text

    def update_date_range(self):
        process_date = self.from_date
        while process_date <= self.to_date:
            self.date_range.append(process_date)
            process_date = process_date + timedelta(days=1)


    def load_index(self, for_date:datetime):
        qtr = math.ceil(float(for_date.strftime("%m")) / 3)
        url = self.base_url + "edgar/daily-index/"
        url += for_date.strftime("%Y") + "/QTR" + str(qtr)
        url += "/master." + for_date.strftime("%Y%m%d") + ".idx"
        resp = self.http_get(url)
        rows = resp.split("\n")
        for row in rows:
            fields = row.split("|")
            if (len(fields) == 5 and '13F-HR' in fields[2]):
                self.index_records.append(fields)


    def load_holdings(self, index_record):
        ret_arr = []
        try:
            filing_url = self.base_url + index_record[4]
            resp = self.http_get(filing_url)
            bad_tags = ["ns1:", "ns2:", "N1:", "n1:", "ns4:", "eis:"]
            for tag in bad_tags:
                resp = resp.replace(tag,"")
            start_pos = resp.find("<informationTable")
            end_pos = resp.find("</informationTable>")
            #print("start end", start_pos,end_pos)
            if start_pos != -1 and end_pos != -1:
                resp = resp[start_pos:end_pos+19]
                #print(resp)
                root = ET.fromstring(resp)
                
                for child in root:
                    rec = []
                    rec.append(index_record[0])    # CIK of Holder
                    rec.append(index_record[1])    # Holder
                    rec.append(index_record[2])    # Form Name
                    rec.append(index_record[3])    # Date filed
                    rec.extend([" "," "," "," "," "," "])
                    #rec.append(index_record[4])    # file name
                    for k in child:
                        tag = k.tag.replace(self.itable,"")
                        if tag == 'nameOfIssuer':
                            rec[4] = k.text
                        if tag == 'titleOfClass':
                            rec[5] = k.text.strip()  
                        if tag == 'cusip':
                            rec[6] = k.text.strip()  
                        if tag == 'value':
                            rec[7] = k.text.strip()      
                        for kc in k:
                            tag = kc.tag.replace(self.itable,"").strip()    
                            #print(tag, kc.tag)
                            if tag == 'sshPrnamt':
                                rec[8] = kc.text.strip()    
                            if tag == 'sshPrnamtType':
                                rec[9] = kc.text.strip()   
                    #print(rec)
                    ret_arr.append(rec)
        except Exception as error:
            print(filing_url, error)

        return ret_arr


    def print_holdings(self):
        header = ["CIK", "HOLDER", "FORM", "DATE_FILED", "HOLDING", "CLASS","CUSIP","VALUE", "QTY", "TYPE"]
        self.update_date_range()
        for dt in self.date_range:
            self.load_index(dt)
        with open(self.data_file, 'w', newline='\n') as csvfile:
            cw = csv.writer(csvfile, delimiter='|',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cw.writerow(header)
            for index_record in self.index_records:
                out = self.load_holdings(index_record)
                filer = index_record[1]
                print(f"{filer.strip():<70} : {len(out):<6} records extracted." )
                for row in out:
                    cw.writerow(row)


