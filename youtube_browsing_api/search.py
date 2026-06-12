""" File containing code for YouTube search operations using InnerTube API """

from typing import Union
from urllib import parse
from .html_scrapper import scrap_request, ScrapResponseData, GOOGLEBOT_HEADERS
from .types import Video, Channel
from .enums import Languages, Regions
from .innertube import Innertube
from .parsers import youtube_search_parse

class Search:
    """
    Class representing search results from YouTube search
    Fields:
    - results # list with searching results (list[Video | Channel])
    - found   # how many results was found  (int)
    """

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

    def __init__(self, query: str, language=Languages.EN, region=Regions.US, timeout=5.0):
        """
        Initializes class object by performing a search request to YouTube
        Arguments:
        - query    [required]
        - language [optional], default = "en"
        - region   [optional], default = "US"
        - timeout  [optional], default = 5.0

        Returns completed Search object on success
        Raises exception on failure
        
        Can raise different exception types, such as:
        - ParserError
        - InvalidStatusError
        and requests.get() exceptions
        """

        self._innertube = Innertube(language, region, timeout=timeout)
        self._query = query # saves query for future use

        self._search()

    def _search(self):
        """
        Internal search method, use .next() method if you want to get next search results,
        or initialize new Search object to perform a new search

        Can raise different exception types, such as:
        - ParserError
        - InvalidStatusError
        and requests.get() exceptions
        """

        request = self._innertube.make_request("search")
        request["query"] = self._query # sets search query
        data = request.perform() # performes a request to YouTube InnerTube API
        self._innertube.cookies = request.cookies # updates cookies

        # parses YouTube response
        self.results: list[Union[Video, Channel]] = youtube_search_parse(data)
        self.found = data["estimatedResults"] # TODO fix, can raise unclear exceptions if this field does not exits


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

    def __init__(self, query: str, language=Languages.EN, region=Regions.US, page=1, timeout=5.0, headers: dict = GOOGLEBOT_HEADERS):
        """
        Initializes class object by performing a search request to YouTube
        Arguments:
        - query    [required]
        - language [optional], default = "en"
        - region   [optional], default = "us"
        - page     [optional], default = 1
        - timeout  [optional], default = 5.0
        - headers  [optional], default = GOOGLEBOT_HEADERS

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

        # saves query, region and language for future use in ._search()
        self._region   :str  = region
        self._query    :str  = query
        self._language :str  = language
        self._headers  :dict = headers
        
        # prepares url and saves it for future use
        self._url = self._make_url(query, page, region)

        self._search() # performes a search

    def _search(self):
        """
        Internal search method, use .next() method if you want to get next search results,
        or initialize new Search object to perform a new search
        It uses internal _headers as fetch headers, _url as url to fetch from, _timeout as request timeout
        """
        scrap_response: ScrapResponseData = scrap_request(self._url, self._headers, self._language, self._timeout)

        self.results: list[Union[Video, Channel]] = youtube_search_parse(scrap_response.data) # results list, clears if it was already filled with items
        self.found: int = scrap_response.data["estimatedResults"] # estimated results count