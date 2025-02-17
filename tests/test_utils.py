from edgar import utils as ut


def test_download():
    ut.download(
        "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/01sep2024-30nov2024_form13f.zip",
        "01sep2024-30nov2024_form13f.zip",
        header={"User-Agent": "nobody@nobody.com", "Accept-Encoding": "gzip, deflate", "Host": "www.sec.gov"},
    )
