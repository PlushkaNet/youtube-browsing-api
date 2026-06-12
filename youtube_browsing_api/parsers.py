""" File containing code for different parsers """

from typing import Union
from .types import Video, Channel, ParserError, ChannelDescription

def youtube_search_parse(data: dict) -> list[Union[Video, Channel]]:
    """ YouTube search deafault (and single for now) parsing method """
    results: list[Union[Video, Channel]] = []

    try:
        section_lists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

        for section_list in section_lists:
            if "itemSectionRenderer" not in section_list:
                continue
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
    except:
        raise ParserError("Parsing entities error\nProbably this because of YouTube updated their endpoints")

    return results


def youtube_channel_parse(data: dict) -> dict:
    """
    Parses channel from YouTube
    Returns complete dict of parsed entities
    Raises ParserError on failure
    """

    result = {}

    try:
        # trying to get banner image url if it exists
        try:
            result["banner_img"] = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['banner']['imageBannerViewModel']['image']['sources'][0]['url']
        except:
            result["banner_img"] = None

        header_content = data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']
        
        result["_desc_continuation_token"] = header_content["description"]["descriptionPreviewViewModel"]["rendererContext"]["commandContext"]["onTap"]["innertubeCommand"]["showEngagementPanelEndpoint"]["engagementPanel"]["engagementPanelSectionListRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]

        result["short_desc"] = header_content["description"]["descriptionPreviewViewModel"]["description"]["content"] # small description part (starting str)
        result["title"] = header_content['title']['dynamicTextViewModel']['text']['content']
        result["subs_count"] = header_content['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content']
        result["thumbnail"] = data['microformat']['microformatDataRenderer']['thumbnail']['thumbnails'][0]['url']

        metadata = data["metadata"]["channelMetadataRenderer"]

        result["desc"] = metadata["description"]
        result["channel_id"] = metadata["externalId"]
        result["keywords"] = metadata["keywords"]
        result["channel_url"] = metadata["channelUrl"]
        result["vanity_channel_url"] = metadata["vanityChannelUrl"]
    except:
        raise ParserError(f"Channel parsing failed\nProbably this because YouTube changed their data endpoints")

    return result

def youtube_channel_description_parse(data: dict) -> ChannelDescription:
    """
    Parses channel description from YouTube
    Returns completed ChannelDescription
    Raises ParserError exception on failure
    """

    try:
        metadata = data["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"][0]["aboutChannelRenderer"]["metadata"]["aboutChannelViewModel"]

        return ChannelDescription(
            metadata["description"],
            metadata["joinedDateText"]["content"],
            metadata["country"]
        )
    except:
        raise ParserError(f"Channel full description parsing failed\nProbably this because YouTube changed their data endpoints")