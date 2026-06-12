""" File containing code for YouTube parsing search operations """

import json
import requests
from urllib import parse
from typing import Union

from .parsers import youtube_search_parse
from .enums import Languages, Regions
from .types import Video, Channel, InvalidStatusError, ExtractorError, JSONParsingError

class SearchFromDocument:
    """
    Class representing search results from YouTube search, extracted from HTML document
    It can be more resistant to some changes in YouTube, but still less preferable than InnerTube API search
    Fields:
    - results # list with searching results (list[Video | Channel])
    - found   # how many results was found  (int)
    - page    # search page                 (int)
    """
    def _make_url(self, query: str, page: int, region: str):
        """ Internal method for prepare url to fetch from """
        return "https://www.youtube.com/results?q=" + parse.quote(query, safe="") + f"&page={page}&gl={region}"
    
    def __iter__(self):
        """ YouTube results iterator """
        yield from self.results

    def as_list(self) -> list[dict]:
        """
        Returns Search as a JSON-like object
        In result, all Video and Channel entries will be converted to dict's
        """
        results: list[dict] = []
        for i in self.results:
            results.append(i.as_dict())

        return results

    def next(self):
        """ Fetches next page of results """
        self.page += 1 # increases page index by 1
        # prepares url
        self._url = self._make_url(self._query, self.page, self._region)
        self._search() # performes a search

    def __init__(self, query: str, language=Languages.EN, region=Regions.US, page=1, timeout=5.0):
        """
        Initializes class object by performing a search request to YouTube
        Arguments:
        - query    [required]
        - language [optional], default = "en"
        - region   [optional], default = "us"
        - page     [optional], default = 1
        - timeout  [optional], default = 5.0

        Returns completed Search object on success
        Raises exception on failure
        
        Can raise different exception types, such as:
        - ExtractorError
        - ParserError
        - InvalidStatusError
        and requests.get() exceptions
        """

        self.page: int = page
        self._timeout: float = timeout # saves timeout for future use in ._search()

        # saves query and region for future use in .next()
        self._region: str = region
        self._query: str = query
        
        # prepares headers for search
        # TODO add headers switch
        self._headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept-Language": language
        }
        
        # prepares url and saves it for future use
        self._url = self._make_url(query, page, region)

        self._search() # performes a search

    def _search(self):
        """
        Internal search method, use .next() method if you want to get next search results,
        or initialize new Search object to perform a new search
        It uses internal _headers as fetch headers, _url as url to fetch from, _timeout as request timeout
        """
        response = requests.get(
            self._url,
            headers=self._headers,
            timeout=self._timeout
        )

        if response.status_code != 200:
            raise InvalidStatusError(response.status_code)

        try:
            try: # Old YouTube parsing first
                data = response.text[response.text.index("ytInitialData")+16::]
                data = data[:data.index('</script>')-1]
            except ValueError: # Scraper-compatible YouTube parsing
                data = response.text[response.text.index("// scraper_data_begin")+42::]
                data = data[:data.index('// scraper_data_end')-3]
        except:
            raise ExtractorError("Extracting error while trying to find ytInitialData or // scrapper_data_begin\nProbably this because page is invalid or YouTube changed their internal extractor")

        try:
            data = json.loads(data) # redefining data here
        except:
            raise JSONParsingError("Failed to parse JSON from YouTube's in-document data")

        self.results: list[Union[Video, Channel]] = youtube_search_parse(data) # results list, clears if it was already filled with items
        self.found: int = data["estimatedResults"] # estimated results count