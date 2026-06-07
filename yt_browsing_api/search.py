from .enums import Languages, Regions
from urllib import parse


def _make_url(query: str, page: int, region: str):
    """ Internal method for prepare url to fetch from """
    return "https://youtube.com/results?q=" + parse.quote(query, safe="") + f"&page={page}&gl={region}"


def search(query: str, language=Languages.EN, region=Regions.US):
    """
    Initializes SearchResults object performing a search
    Arguments:
    - query    [required]
    - language [optional], default = "en"
    - region   [optional], default = "us"

    Returns completed SearchResults on success
    Returns None on fail
    """