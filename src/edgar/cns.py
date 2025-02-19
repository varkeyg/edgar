# https://www.sec.gov/files/data/fails-deliver-data/cnsfails202501a.zip
# https://www.sec.gov/files/data/fails-deliver-data/cnsfails202501a.zip
from datetime import datetime, timedelta
from edgar import utils as ut
from dotenv import load_dotenv
import os
import csv

class cns:
    def __init__(self):
        load_dotenv(verbose=True)
        self.cns_folder = os.getenv("data_folder") + "/cns"
        os.makedirs(self.cns_folder, exist_ok=True)
        self.sec_header = {"User-Agent": "nobody@nobody.com", "Accept-Encoding": "gzip, deflate", "Host": "www.sec.gov"}
        self.cns_files = []
        self.base_url = "https://www.sec.gov/files/data/fails-deliver-data/cnsfails"
        # pass

    def load_urls(self, num_months=12):
        today = datetime.today().strftime("%Y%m01")
        first_of_month = datetime.strptime(today, "%Y%m%d")
        # print(today, first_of_month)
        for x in range(num_months):
            for a in ["a", "b"]:
                url = self.base_url + first_of_month.strftime("%Y%m") + a + ".zip"
                # print(url)
                local_file = self.cns_folder + "/" + url.split("/")[-1]
                ut.download(url, local_file, header=self.sec_header)
                try:
                    ut.unzip(local_file, self.cns_folder)
                    self.cns_files.append(local_file.replace(".zip",""))
                except Exception:
                    pass
            first_of_month = first_of_month - timedelta(days=30)

    def combine_files(self):
        header = ["SETTLEMENT_DATE", "CUSIP", "SYMBOL", "QUANTITY","DESCRIPTION" , "PRICE"]
        with open(self.cns_folder + "/cns.csv","w") as w:
            writer = csv.writer(w)
            writer.writerow(header)
            for data_file in self.cns_files:
                with open(data_file,"r") as df:
                    reader = csv.reader(df, delimiter="|")  
                    next(reader)    
                    for row in reader:
                        if len(row) == 6:
                            writer.writerow(row)
