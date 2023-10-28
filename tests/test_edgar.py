from edgar import edgar

def test_holdings_export():
    e = edgar.Edgar("20231024","20231024")
    e.print_holdings()
    pass



