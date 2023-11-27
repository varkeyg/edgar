import requests
import os
import psycopg
import csv
import shutil
from zipfile import ZipFile 
import time
import sys
import urllib.request
from urllib.request import Request, urlopen

def file2string(filename) -> str:
    with open(filename, 'r') as f:
        return f.read()


def csv2list(filename, delim=','):
    rs = Recordset()
    with open(filename) as f:
        csvreader = csv.reader(f,delimiter=delim)
        for idx, row in enumerate(csvreader):
            if idx == 0:
                rs.add_header(list(row))
            else:
                if len(row) == len(rs.header):
                    rs.add_row(row)
        return rs


def download(url, outfile, header=None):
    print("\nDownloading", url)
    r = requests.get(url, headers=header )
    with open(outfile, "wb") as w:
        w.write(r.content)



def unzip(zipfile, folder):
    try:
        with ZipFile(zipfile, 'r') as z:
            z.extractall(path=folder)
    except:
        pass




class Recordset:
    def __init__(self) -> None:
        self.header = []
        self.records = []

    def add_header(self, header):
        _header = []
        for field in header:
            field = field.replace("*", "")
            field = field.replace(" ", "_")
            field = field.replace("(", "")
            field = field.replace(")", "")
            field = field.lower()
            _header.append(field)
        self.header = _header

    def add_row(self, row: list):
        self.records.append(row)


class PGDB:
    def __init__(self, dburi) -> None:
        self.con = psycopg.connect(dburi)

    def runsql_script(self, sql_file):
        s = file2string(sql_file)
        sqls = s.split(";")
        for sql in sqls:
            self.runsql(sql)
        

    def runsql(self, sql, params=None):
        cur = self.con.cursor()
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params=params)
        self.con.commit()
        cur.close()

    def get_table_ddl(self, rs: Recordset, table_name: str):
        sql = "create table " + table_name + "\n(\n"
        for field in rs.header:
            width = (len(field) + 2000) * 2
            sql += f"    {field:{20}} varchar({width}),\n"
        sql = sql[:-2]
        sql += "\n)\n"
        return sql

    def save2db(self, rs: Recordset, table_name: str, recreate=True):
        create_sql = self.get_table_ddl(rs, table_name)
        if recreate:
            self.runsql("drop table if exists " + table_name)
            self.runsql(create_sql)
        cur = self.con.cursor()
        ins_sql = "insert into " + table_name + " values ( "
        for i in range(len(rs.header)):   
            ins_sql += "%s, "
        ins_sql = ins_sql[:-2]
        ins_sql += " ) "
        cur.executemany(ins_sql, rs.records)
        self.con.commit()
        cur.close()
    
    def runquery(self,query, params=None):
        rs = Recordset()
        cur = self.con.cursor()
        if params is None:
            cur.execute(query=query)
        else:
            cur.execute(query=query, params=params)
        header = []
        for field in cur.description:
            header.append(field.name)
        rs.add_header(header=header)
        for row in cur:
            rs.add_row(list(row))
        cur.close()
        return rs

    def runquery_file(self, query_file, params=None):
        sql = file2string(query_file)
        if params is None:
            return self.runquery(sql)
        else:
            return self.runquery(sql, params)
            
    


def write_graph_data(rs:Recordset, outfile:str, write_header=False):
    new_header = []
    for idx,field in enumerate(rs.header):
        if field == "id":
            field = ":ID"
        elif field == "label":
            field = ":LABEL" 
        elif field == "start_id":
            field = ":START_ID" 
        elif field == "end_id":
            field = ":END_ID"
        elif field == "type":
            field = ":TYPE"
        field = field.replace(":string",":String")
        field = field.replace(":double",":Double")
        field = field.replace(":datetime",":DateTime")
        new_header.append(field)
    rs.header = new_header

    mode = ''
    if write_header is True:
        mode = 'w'
    else:
        mode = 'a'
    with open(outfile, mode, newline='\n') as csvfile:
        cw = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if write_header is True:
            cw.writerow(rs.header)
        for record in rs.records:
            cw.writerow(record)