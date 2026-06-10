""" File containing code for YouTube search operations """

import json
import requests
from urllib import parse
from typing import Union

from .enums import Languages, Regions
from .types import Video, Channel, InvalidStatusError, ExtractorError, ParserError

class Search:
    """
    Class representing search results from YouTube search
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

        # googlebot user agent
        # TODO add headers switch
        self._headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept-Language": language
        }

        self._url = self._make_url(query, page, region) # makes url and saves it for future use

        response = requests.get(
            self._url,
            headers=self._headers,
            timeout=timeout
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

            self.results: list[Union[Video, Channel]] = [] # results list
            self.found: int = data["estimatedResults"] # estimated results count
            self.page: int = page # page of search
            
            section_lists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

            for section_list in section_lists:
                if "itemSectionRenderer" not in section_list: continue
                for content in section_list["itemSectionRenderer"]["contents"]:
                    try:
                        try:
                            # trying to get it here to skip doubling later
                            account_type = content["videoRenderer"]["ownerBadges"][0]["metadataBadgeRenderer"]["style"]
                        except:
                            account_type = "regular"
                        if "videoRenderer" in content.keys():
                            self.results.append(
                                Video(
                                    content["videoRenderer"]["videoId"],
                                    content["videoRenderer"]["title"]["runs"][0]["text"],
                                    content["videoRenderer"]["ownerText"]["runs"][0]["text"],
                                    content["videoRenderer"]["lengthText"]["simpleText"],
                                    content["videoRenderer"]["viewCountText"]["simpleText"],
                                    content["videoRenderer"]["publishedTimeText"]["simpleText"],
                                    content["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"], # best quality
                                    content["videoRenderer"]["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][0]["url"],
                                    content["videoRenderer"]["detailedMetadataSnippets"][0]["snippetText"]["runs"][0]["text"],
                                    account_type
                                )
                            )
                        
                        elif "channelRenderer" in content.keys():
                            self.results.append(
                                Channel(
                                    content["channelRenderer"]["channelId"],
                                    content["channelRenderer"]["title"]["simpleText"],
                                    content["channelRenderer"]["videoCountText"]["accessibility"]["accessibilityData"]["label"],
                                    content["channelRenderer"]["thumbnail"]["thumbnails"][0]["url"], # starts with //
                                    account_type
                                )
                            )
                    except:
                        continue
        except:
            raise ParserError("Parsing entities error\nProbably this because of YouTube updated their endpoints")