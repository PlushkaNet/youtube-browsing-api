from typing import Optional
import json
import requests

from .types import ChannelInfo
from .enums import Languages

def _make_url(query: str):
    """ Internal method for prepare channel url to fetch from """
    return "https://www.youtube.com/@" + query.removeprefix("@")


def get_channel(channel_id: str, language=Languages.EN, timeout=5.0) -> Optional[ChannelInfo]:
    """
    Gets information about channel
    Arguments:
    - channel_id [required]
    - language   [optional], default = "en"
    - timeout    [optional], default = 5.0

    Returns completed ChannelInfo on success
    Returns None on fail
    """

    # googlebot user agent
    # TODO add headers switch
    headers= {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Accept-Language": language
    }

    try:
        response = requests.get(
            _make_url(channel_id),
            headers=headers,
            timeout=timeout
        )
    except:
        return None

    if response.status_code != 200: return None

    # TODO merge parsing for search and get_channel into single parse method

    try: # Old YouTube parsing
        data = response.text[response.text.index("ytInitialData")+16::]
        data = data[:data.index('</script>')-1]
    except ValueError: # Scraper-compatible YouTube parsing
        data = response.text[response.text.index("// scraper_data_begin")+42::]
        data = data[:data.index('// scraper_data_end')-3]

    try:
        data = json.loads(data)
        
        try:
            banner_img = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['banner']['imageBannerViewModel']['image']['sources'][0]['url']
        except:
            banner_img = None

        page_header_view_model = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']

        channel_info = ChannelInfo(
            page_header_view_model['title']['dynamicTextViewModel']['text']['content'],
            page_header_view_model['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'],
            data['microformat']['microformatDataRenderer']['thumbnail']['thumbnails'][0]['url'],
            banner_img
        )
    except:
        return None

    return channel_info