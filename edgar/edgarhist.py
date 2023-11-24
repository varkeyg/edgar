import configparser
import os
from common import utils
import csv
import datetime
from dateutil.relativedelta import relativedelta 
import math
import json
from pathlib import Path

class EdgarHist:
    def __init__(self,num_quarters=1) -> None:
        self.config = configparser.ConfigParser()
        config_file = os.path.join(os.path.dirname(__file__), "config.ini")
        self.ref_folder = str(Path(__file__).resolve().parent.parent) + "/reference/"
        self.config.read(config_file)
        self.header = {"User-Agent" : "Me Inc noname@me.inc", "Accept-Encoding" : "gzip, deflate", "Host" : "www.sec.gov"}
        self.data_folder = str(Path(__file__).resolve().parent.parent) + "/" + self.config["storage"]["data-folder"]
        self.pgdb = utils.PGDB(self.config["pgdb"]["dburi"])
        self.num_quarters = num_quarters
        self.quater_strings = []
        self.load_quaters()
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)


    def load_quaters(self):
        today = datetime.date.today()
        for i in range(self.num_quarters):
            self.quater_strings.append(str(today.year) + "q" + str(math.ceil((today.month/3))))
            today = today - relativedelta(months=3)
        self.quater_strings.pop(0)
    
            
    def load_sic_codes(self):
        rs = utils.csv2list(self.ref_folder + "sic_code.csv")
        self.pgdb.save2db(rs, 'sec_sic')

    def load_cik_sic_codes(self):
        rs = utils.csv2list(self.ref_folder + "cik-sic.csv")
        self.pgdb.save2db(rs, 'sec_cik_sic')

 

    def download13f(self):
        for year_quarter in self.quater_strings:
            url = self.config["edgar"]["13f"] + year_quarter + "_form13f.zip"
            outfile = self.data_folder + os.path.basename(url)
            utils.download(url, outfile=outfile, header=self.header)
            outfolder = self.data_folder + os.path.basename(url).replace(".zip","")
            utils.unzip(self.data_folder + year_quarter + "_form13f.zip", outfolder)
    
    def load_infotable(self):
        recreate = True
        for idx,q in enumerate(self.quater_strings):
            if idx > 0:
                recreate = False
            rs = utils.csv2list(self.data_folder + q + '_form13f/INFOTABLE.tsv','\t')
            self.pgdb.save2db(rs, 'sec_13f_infotable',recreate=recreate)
            rs = utils.csv2list(self.data_folder + q + '_form13f/SUBMISSION.tsv','\t')
            self.pgdb.save2db(rs, 'sec_13f_submission',recreate=recreate)
            rs = utils.csv2list(self.data_folder + q + '_form13f/COVERPAGE.tsv','\t')
            self.pgdb.save2db(rs, 'sec_13f_coverpage',recreate=recreate)
