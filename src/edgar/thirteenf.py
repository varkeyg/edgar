from dotenv import load_dotenv
import os
from edgar import utils as ut
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET


class ThirteenF:
    def __init__(self):
        load_dotenv(verbose=True)
        self.tf_folder = os.getenv("data_folder") + "/thirteenf"
        os.makedirs(self.tf_folder, exist_ok=True)
        self.min_date = datetime.fromisoformat("2025-02-10")
        self.filing_dates = []
        self.filing_urls = []
        self.directories = []
        self.sec_header = {"User-Agent": "nobody@nobody.com", "Accept-Encoding": "gzip, deflate", "Host": "www.sec.gov"}
        self.base_index_url = "https://www.sec.gov/Archives/edgar/daily-index/"  # 2025/QTR1/master.20250214.idx"
        print("Initialized thirteenf")

    def get_urls(self, num_quarters):
        urls = []
        base_url = "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/"
        quarters = []
        quarters.append("01sep2024-30nov2024_form13f.zip")
        quarters.append("01jun2024-31aug2024_form13f.zip")
        quarters.append("01mar2024-31may2024_form13f.zip")
        quarters.append("01jan2024-29feb2024_form13f.zip")
        quarters.extend(["2023q4_form13f.zip", "2023q3_form13f.zip", "2023q2_form13f.zip", "2023q1_form13f.zip"])
        quarters.extend(["2022q4_form13f.zip", "2022q3_form13f.zip", "2022q2_form13f.zip", "2022q1_form13f.zip"])
        for x in range(0, num_quarters):
            urls.append(f"{base_url}{quarters[x]}")
        return urls

    def download_files(self, urls):
        for url in urls:
            zip_file = url.split("/")[-1]
            zip_dir = (url.split("/")[-1]).replace(".zip", "")
            local_dir = self.tf_folder + "/" + zip_dir + "/"
            os.makedirs(local_dir, exist_ok=True)
            self.directories.append(local_dir)
            ut.download(url, local_dir + zip_file, self.sec_header)

    def unzip(self):
        for dir in self.directories:
            zip_file = dir + "/" + dir.split("/")[-2] + ".zip"
            ut.unzip(zip_file, dir)

    def get_13f_data(self):
        self.get_new_filing_dates()
        for dt in self.filing_dates:
            qtr = (dt.month - 1) // 3 + 1
            index_url = f"{self.base_index_url}{dt.year}/QTR{qtr}/master.{dt.strftime('%Y%m%d')}.idx"  # 2025/QTR1/master.20250214.idx"
            self.extract_13f_urls(index_url=index_url)
        print(f"number of 13F filings {len(self.filing_urls)}")
        for filing in self.filing_urls[0:10]:
            self.extract_holdings(filing)

    def extract_13f_urls(self, index_url):
        resp = requests.get(index_url, headers=self.sec_header)
        if resp.status_code == 200:
            lines = resp.text.split("\n")
            for line in lines:
                record = line.split("|")
                if len(record) == 5:
                    if record[2].startswith("13F"):
                        self.filing_urls.append(record)

    def get_new_filing_dates(self):
        cur_date = datetime.today()
        while cur_date >= self.min_date:
            self.filing_dates.append(cur_date)
            cur_date = cur_date + timedelta(days=-1)

    def extract_holdings(self, filing):
        url_13f = f"https://www.sec.gov/Archives/{filing[4]}"
        resp = requests.get(url_13f, headers=self.sec_header)
        header = self.extract_header(resp.text)
        raw_filing = resp.text
        raw_filing = raw_filing.replace("ns1:", "")
        raw_filing = raw_filing.replace("ns2:", "")
        raw_filing = raw_filing.replace("ns3:", "")
        raw_filing = raw_filing.replace("ns4:", "")
        info_table_start = raw_filing.find("<informationTable")
        info_table_end = raw_filing.find("</informationTable>") + 19
        holdings = raw_filing[info_table_start:info_table_end]
        root = ET.fromstring(holdings)
        for infotable in root.findall("infoTable"):
            rec = []
            rec.extend(filing)
            rec.append(self.nvl(infotable.find("nameOfIssuer")))
            rec.append(self.nvl(infotable.find("titleOfClass")))
            rec.append(self.nvl(infotable.find("cusip")))
            rec.append(self.nvl(infotable.find("figi")))
            rec.append(self.nvl(infotable.find("value")))
            shrsOrPrnAmt = infotable.find("shrsOrPrnAmt")
            if shrsOrPrnAmt is not None:
                rec.append(self.nvl(shrsOrPrnAmt.find("sshPrnamt")))
                rec.append(self.nvl(shrsOrPrnAmt.find("sshPrnamtType")))
            else:
                rec.append("")
                rec.append("")
            rec.append(self.nvl(infotable.find("investmentDiscretion")))
            votingAuthority = infotable.find("votingAuthority")
            if votingAuthority is not None:
                rec.append(self.nvl(votingAuthority.find("Sole")))
                rec.append(self.nvl(votingAuthority.find("Shared")))
                rec.append(self.nvl(votingAuthority.find("None")))
            else:
                rec.append("")
                rec.append("")
                rec.append("")
            rec.extend(header)
            print(rec)

    def nvl(self, x):
        return "" if x is None else x.text

    def extract_header(self, filing):
        header = []
        lines = filing.split("\n")
        for line in lines:
            if line.startswith("</SEC-HEADER>"):
                break
            if line.startswith("ACCESSION NUMBER:"):
                header.append(line.replace("ACCESSION NUMBER:","").strip())
            if line.startswith("CONFORMED PERIOD OF REPORT:"):
                header.append(line.replace("CONFORMED PERIOD OF REPORT:","").strip())    
            if line.startswith("FILED AS OF DATE:"):
                header.append(line.replace("FILED AS OF DATE:","").strip())    
            if line.startswith("DATE AS OF CHANGE:"):
                header.append(line.replace("DATE AS OF CHANGE:","").strip())   
            if line.startswith("EFFECTIVENESS DATE:"):
                header.append(line.replace("EFFECTIVENESS DATE:","").strip())                              
        return header