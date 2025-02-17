from edgar import thirteenf


def test_13f():
    tf = thirteenf.ThirteenF()
    # urls = tf.get_urls(4)
    # tf.download_files(urls)
    # tf.unzip()
    tf.get_13f_data()
