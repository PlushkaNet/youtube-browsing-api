""" File containing code for YouTube search operations using InnerTube API """

from typing import Union
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