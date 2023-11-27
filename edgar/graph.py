from common import utils
from pathlib import Path
import configparser
import os

class Export:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        config_file = os.path.join(os.path.dirname(__file__), "config.ini")
        self.config.read(config_file)
        self.sql_folder = str(Path(__file__).resolve().parent.parent) + "/sql/"
        self.graph_data_folder = str(Path(__file__).resolve().parent.parent) + "/data/graph_data/"
        self.pgdb = utils.PGDB(self.config["pgdb"]["dburi"])
        if not os.path.exists(self.graph_data_folder):
            os.makedirs(self.graph_data_folder)

    def export_sic_nodes(self):
        sql_file = self.sql_folder + "nodes_sic.sql"
        rs = self.pgdb.runquery_file(sql_file)
        utils.write_graph_data(rs, self.graph_data_folder + "/sic_nodes.csv")

    def export_cik_nodes(self):
        sql_file = self.sql_folder + "nodes_cik.sql"
        rs = self.pgdb.runquery_file(sql_file)
        utils.write_graph_data(rs, self.graph_data_folder + "/cik_nodes.csv")

    def export_cusip_nodes(self):
        sql_file = self.sql_folder + "nodes_cusip.sql"
        drs = self.pgdb.runquery("select distinct filing_date from public.sec_13f_submission")
        for idx,rec in enumerate(drs.records):            
            rs = self.pgdb.runquery_file(sql_file,params=rec)
            print(idx, rec, len(rs.records), "records")
            if idx == 0:
                utils.write_graph_data(rs, self.graph_data_folder + "/cusip_nodes.csv", write_header=True)
            else:
                utils.write_graph_data(rs, self.graph_data_folder + "/cusip_nodes.csv", write_header=False)

    def export_cik_sic_edges(self):
        sql_file = self.sql_folder + "edges_cik_sic.sql"
        rs = self.pgdb.runquery_file(sql_file)
        utils.write_graph_data(rs, self.graph_data_folder + "/cik_sic_edges.csv")
 
    def export_cik_cusip_edges(self):
        sql_file = self.sql_folder + "edges_cik_cusip.sql"
        drs = self.pgdb.runquery("select distinct filing_date from public.sec_13f_submission")
        for idx,rec in enumerate(drs.records):  
            rs = self.pgdb.runquery_file(sql_file,params=rec)
            print(idx, rec, len(rs.records), "records - edges_cik_cusip")
            if idx == 0:
                utils.write_graph_data(rs, self.graph_data_folder + "/cik_cusip_edges.csv", write_header=True)
            else:
                utils.write_graph_data(rs, self.graph_data_folder + "/cik_cusip_edges.csv", write_header=False)
 

def run():
    x = Export()
    x.export_sic_nodes()
    x.export_cik_nodes()
    x.export_cusip_nodes()
    x.export_cik_sic_edges()
    x.export_cik_cusip_edges()

    