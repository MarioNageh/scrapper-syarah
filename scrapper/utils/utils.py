from urllib.parse import unquote


def get_url_without_encoding(url):
    return unquote(url)
