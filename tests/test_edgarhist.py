from edgar import edgarhist


# poetry run pytest -s tests/test_edgarhist.py -k 'test_load' -q
def test_load():
    x = edgarhist.EdgarHist(num_quarters=8)
    x.load_sic_codes()
    x.load_cik_sic_codes()
    x.download13f()
    x.load_infotable()