from edgar import thirteenf
from edgar import cns
import os

def test_13f():
    tf = thirteenf.ThirteenF()
    # urls = tf.get_urls(4)
    # tf.download_files(urls)
    # tf.unzip()
    # tf.get_13f_data()
    # print("PWD", os.getcwd())
    tf.generate_ddl("resources/FORM13F_metadata.json")

def test_cns():
    c = cns.cns()
    c.load_urls(num_months=12)
    c.combine_files()