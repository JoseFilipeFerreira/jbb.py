import urllib


def make_url(query):
    return urllib.parse.quote(' '.join(query), safe='')
