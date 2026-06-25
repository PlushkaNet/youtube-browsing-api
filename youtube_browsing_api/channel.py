# pylint: disable=C0301
"""File containing code for YouTube channels operations"""

from typing import Optional
from .innertube import Innertube, InnertubeRequest
from .parsers import youtube_channel_parse, youtube_channel_description_parse
from .html_scrapper import scrap_request, GOOGLEBOT_HEADERS, ScrapResponseData
from .enums import Languages
from .types import ChannelDescription

class GetChannelInfo:
    """
    Class representing full info about YouTube channel
    In difference from Channel, ChannelInfo contains advanced info about channel, unavaliable from search

    Fields:
    `title` is a channel title from YouTube
    `subs_count` is a counter with word quantifiers how many subscribers does channel have, example: "123 million subscribers"
    `thumbnail` is a channel's image url to internal YouTube storage in high quality
    `short_desc` is a channel's small part of description. It appears at channel preview on YouTube, example: "NCS is on a mission to soundtrack the internet. 🚀", but full description is much larger
    `desc` is a channel's description. Can be empty string if author didn't set their's channel description
    `full_desc` is a channel's descrition object. It's None by default, because requires to fetch some additional data. Can be requested by calling fetch_description()
    `banner_img` is a channel's header banner image url in hight quality. Can be None if channel doesn't have banner
    `channel_id` is a channel's ID like UC_aEa8K-EOJ3D6gOs7HcyNg (NCS)
    `channel_url` is a channel's URL like https://www.youtube.com/channel/UC_aEa8K-EOJ3D6gOs7HcyNg (NCS)
    `vanity_channel_url` is a channel's URL like https://www.youtube.com/@NoCopyrightSounds
    `keywords` are channel's related keywords, example: ["music songs ncs", "no copyright music", "edm", "copyright free music"]
    """

    def __init__(self, channel: str, language=Languages.EN, timeout=5.0, headers: dict = GOOGLEBOT_HEADERS):
        """
        Initializes class object by performing a request to the channel page
        Arguments:
        - channel    [required]
        - language   [optional], default = "en"
        - timeout    [optional], default = 5.0
        - headers    [optional], default = GOOGLEBOT_HEADERS
        
        `channel` can be valid YouTube URL to channel, @Username or channel ID like `UC_aEa8K-EOJ3D6gOs7HcyNg` (NCS)"

        `headers` are used only if performing a request to HTML document to parse

        Returns completed GetChannelInfo on success
        Raises exception on failure
        """
        
        self._innertube = Innertube(hl=language, timeout=timeout) # initializing Innertube client for future use

        if channel.startswith("http") or channel.startswith("@"):
            # processing with scrap-document request
            if channel.startswith("@"):
                url: str = "https://www.youtube.com/" + channel
            else:
                url: str = channel
            
            scrap_response: ScrapResponseData = scrap_request(url, headers, language, timeout)

            data = scrap_response.data
            self._innertube.cookies = scrap_response.cookies # saving cookies for future use
        else:
            # processing with InnerTube request
            request: InnertubeRequest = self._innertube.make_request("browse")
            request["browseId"] = channel

            data = request.perform()
            self._innertube.cookies = request.cookies
        
        # parse data
        channel_info = youtube_channel_parse(data)
        
        # extracting dict fields into class object's fields
        self.title: str = channel_info["title"]
        self.subs_count: str = channel_info["subs_count"]
        self.thumbnail: str = channel_info["thumbnail"]
        self.short_desc: str = channel_info["short_desc"]
        self.desc: str = channel_info["desc"]
        self.banner_img: str = channel_info["banner_img"]
        self.channel_id: str = channel_info["channel_id"]
        self.channel_url: str = channel_info["channel_url"]
        self.keywords: str = channel_info["keywords"]
        self.vanity_channel_url: str = channel_info["vanity_channel_url"]

        self.full_desc: Optional[ChannelDescription] = None

        self._data = channel_info # save for future use
        
    def fetch_description(self):
        """
        Fetches channel descritpion and saves it to `full_desc` field
        `full_desc` field have type of ChannelDescription or None (if failed)
        Returns self if success
        Raises an exception on failure
        """

        request: InnertubeRequest = self._innertube.make_request("browse")
        request["context"]["client"]["mainAppWebInfo"] = {
            "graftUrl": self.vanity_channel_url
        }
        request["continuation"] = self._data["_desc_continuation_token"]

        data = request.perform()

        self.full_desc: ChannelDescription = youtube_channel_description_parse(data)

        return self
