from typing import Optional
import json
import requests

from .enums import Languages, Regions
from .types import ChannelDescription

class GetChannelInfo:
    """
    Class representing full info about YouTube channel
    In difference from Channel, ChannelInfo contains advanced info about channel, unavaliable from search

    Fields:
    - title      [str]
    - subs_count [str]
    - thumbnail  [str]
    - desc       [ChannelDescription | None]
    - banner_img [str]

    [title] is a channel title
    [subs_count] is a counter with word quantifiers how many subscribers does channel have, often looks like: "123 million subscribers"
    [thumbnail] is a channel image url in high quality
    [desc] is a channel descrition object if initialized by calling fetch_description(), or None (by default)
    [banner_img] is a channel's header banner image url in hight quality

    Secured fields:
    - _url                     # YouTube channel URL
    - _desc_continuation_token # Continuation token for fetching full channel description
    - _cookies                 # Response cookies from YouTube
    - _headers                 # Request headers
    """

    __slots__ = ["title", "subs_count", "thumbnail", "desc", "banner_img", "_url", "_desc_continuation_token", "_cookies", "_headers"]

    def _make_url(self, query: str) -> str:
        """ Internal method for prepare channel url to fetch from """
        return "https://www.youtube.com/@" + query.removeprefix("@")
    

    def __init__(self, channel_id: str, language=Languages.EN, timeout=5.0):
        """
        Initializes class object by performing a request to the channel page
        Arguments:
        - channel_id [required]
        - language   [optional], default = "en"
        - timeout    [optional], default = 5.0

        Returns completed GetChannelInfo on success
        Raises exception on failure
        """

        # googlebot user agent; saves it for future use
        # TODO add headers switch
        self._headers= {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept-Language": language
        }

        # makes valid youtube channel url to fetch from and saves it for future use
        self._url = self._make_url(channel_id)

        response = requests.get(
            self._url,
            headers=self._headers,
            timeout=timeout
        )

        if response.status_code != 200:
            raise Exception(f"Get page response status code is {response.status_code}")
        
        # TODO merge parsing for search and get_channel into single parse method

        try: # Old YouTube parsing
            data = response.text[response.text.index("ytInitialData")+16::]
            data = data[:data.index('</script>')-1]
        except ValueError: # Scraper-compatible YouTube parsing
            data = response.text[response.text.index("// scraper_data_begin")+42::]
            data = data[:data.index('// scraper_data_end')-3]

        try:
            data = json.loads(data)

            # trying to get banner image url if it exists
            try:
                self.banner_img: Optional[str] = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['banner']['imageBannerViewModel']['image']['sources'][0]['url']
            except:
                self.banner_img: Optional[str] = None
            
            # page_header_view_model["description"]["descriptionPreviewViewModel"]["description"]["content"] # small description part (starting str)

            header_content = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']
            
            self._desc_continuation_token: str = header_content["description"]["descriptionPreviewViewModel"]["rendererContext"]["commandContext"]["onTap"]["innertubeCommand"]["showEngagementPanelEndpoint"]["engagementPanel"]["engagementPanelSectionListRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            self._cookies = response.cookies

            self.title      :str = header_content['title']['dynamicTextViewModel']['text']['content']
            self.subs_count :str = header_content['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content']
            self.thumbnail  :str = data['microformat']['microformatDataRenderer']['thumbnail']['thumbnails'][0]['url']

            self.desc: Optional[ChannelDescription] = None
        except Exception as e:
            raise Exception(f"Parsing error: {e}")

        
    def fetch_description(self, language=Languages.EN, region=Regions.US, timeout=5.0):
        """
        Fetches channel descritpion and saves it to [desc] field
        [desc] field have type of ChannelDescription or None (if failed)
        Arguments:
        - channel_id [required]
        - language   [optional], default = "en"
        - timeout    [optional], default = 5.0

        Returns self if success
        Raises an exception on failure
        """

        try:
            rollout_token   : str = self._cookies["__Secure-ROLLOUT_TOKEN"]
            visitor_metadata: str = self._cookies["VISITOR_PRIVACY_METADATA"]
        except:
            raise Exception("Cannot get required credentials from cookies")
        
        # JSON payload for fetching channel full desctiption
        post_data = {
            "context": {
                "client": {
                    "browserName": "Chrome",
                    "browserVersion": "148.0.0.0",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "clientName": "WEB",
                    "clientVersion": "2.20260606.02.00", # some client
                    "gl": region.upper(),
                    "hl": language,
                    "mainAppWebInfo": {
                        "graftUrl": self._url
                    },
                    "rolloutToken": rollout_token,
                    "visitorData": visitor_metadata
                },
                "request": {
                    "useSsl": True
                }
            },
            "continuation": self._desc_continuation_token
        }
    
        response = requests.post(
            "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false",
            cookies=self._cookies,
            headers=self._headers,
            json=post_data
        )

        if response.status_code != 200:
            raise Exception(f"Response status is {response.status_code}\n{response.text}\n\n{self._desc_continuation_token}\n\n{self._url}\n\n{rollout_token}\n\n{visitor_metadata}\n\n{response.request.body}")

        data = json.loads(response.text)

        try:
            metadata = data["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"][0]["aboutChannelRenderer"]["metadata"]["aboutChannelViewModel"]

            self.desc = ChannelDescription(
                metadata["description"],
                metadata["joinedDateText"]["content"],
                metadata["country"]
            )
        except:
            raise Exception("Failed to parse response from YouTube. Probably its because they have updated their extraction scheme")

        return self