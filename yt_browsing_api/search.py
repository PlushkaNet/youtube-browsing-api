""" File containing code for YouTube search operations """

import json
import requests
from urllib import parse
from typing import Union, Optional

from .enums import Languages, Regions
from .types import Video, Channel, SearchResults


def _make_url(query: str, page: int, region: str):
    """ Internal method for prepare url to fetch from """
    return "https://www.youtube.com/results?q=" + parse.quote(query, safe="") + f"&page={page}&gl={region}"


def search(query: str, language=Languages.EN, region=Regions.US, page=1, timeout=5.0) -> Optional[SearchResults]:
    """
    Performes a search
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

    try:
        response = requests.get(
            _make_url(query, page, region),
            headers=headers,
            timeout=timeout
        )
    except:
        return None

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
                        results.append(
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
                        results.append(
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

        search_results = SearchResults(results, data["estimatedResults"], page)
    except:
        return None

    return search_results