# pylint: disable=C0301
"""
File containing code for requesting and scraping data from YouTube HTML pages
"""

import json
from dataclasses import dataclass
import requests
from requests.cookies import CookieJar
from .types import InvalidStatusError, ExtractorError, JSONParsingError
from .enums import Languages

GOOGLEBOT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

@dataclass
class ScrapResponseData:
    """ Class for serving data from scraper method """
    data    :dict
    cookies :CookieJar

def scrap_request(url: str, headers: dict = GOOGLEBOT_HEADERS, language: str = Languages.EN, timeout: float = 5.0) -> ScrapResponseData:
    """
    Performes a request to specified URL and scraps data from page
    If it don't works with default Googlebot headers, try to pass headers from browser
    Arguments:
    - url       [required]
    - headers,  [optional], default = GOOGLEBOT_HEADERS
    - language, [optional], default = "en"
    - timeout,  [optional], default = 5.0
    """
    headers["Accept-Language"] = language # changes headers Accept-Language on provided
    response = requests.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InvalidStatusError(response.status_code)

    # tryes to srcap data from document
    try:
        try: # Old YouTube parsing first
            data = response.text[response.text.index("ytInitialData")+16::]
            data = data[:data.index('</script>')-1]
        except ValueError: # Scraper-compatible YouTube parsing
            data = response.text[response.text.index("// scraper_data_begin")+42::]
            data = data[:data.index('// scraper_data_end')-3]
    except ValueError as e:
        raise ExtractorError("Extracting error while trying to find ytInitialData or // scrapper_data_begin\nProbably this because page is invalid or YouTube changed their internal extractor") from e

    try:
        data = json.loads(data) # replaces raw data with JSON extracted dict data
    except json.JSONDecodeError as e:
        raise JSONParsingError("Failed to parse JSON from YouTube's in-document data") from e

    return ScrapResponseData(data, response.cookies)
