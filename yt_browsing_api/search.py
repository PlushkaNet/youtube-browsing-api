import json
import requests
from urllib import parse
from typing import Union

from .enums import Languages, Regions
from .types import Video, Channel


def _make_url(query: str, page: int, region: str):
    """ Internal method for prepare url to fetch from """
    return "https://youtube.com/results?q=" + parse.quote(query, safe="") + f"&page={page}&gl={region}"


def search(query: str, language=Languages.EN, region=Regions.US, page=1, timeout=5.0):
    """
    Initializes SearchResults object performing a search
    Arguments:
    - query    [required]
    - language [optional], default = "en"
    - region   [optional], default = "us"
    - page     [optional], default = 1
    - timeout  [optional], default = 5.0

    Returns completed SearchResults on success
    Returns None on fail
    """

    # googlebot user agent
    # TODO add headers switch
    headers= {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Accept-Language": language
    }

    results: list[Union[Video, Channel]] = []

    response = requests.get(
        _make_url(query, page, region),
        headers=headers,
        timeout=timeout)

    if response.status_code != 200: return None

    try: # Old YouTube parsing first
        data = response.text[response.text.index("ytInitialData")+16::]
        data = data[:data.index('</script>')-1]
    except ValueError: # Scraper-compatible YouTube parsing
        data = response.text[response.text.index("// scraper_data_begin")+42::]
        data = data[:data.index('// scraper_data_end')-3]

    try:
        data = json.loads(data)
        section_lists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    except:
        return None

    if type(section_lists) != list:
        return None

    for section_list in section_lists:
        if type(section_list) != dict or "itemSectionRenderer" not in section_list: continue
        