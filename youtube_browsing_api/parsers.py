""" File containing code for different parsers """

from typing import Union, Any
from .types import Video, Channel, ParserError, ChannelDescription, LinkIcon

def youtube_search_contents_parse(contents: list) -> list[Union[Channel, Video]]:
    """
    Parses videos and channels from itemSectionRenderer.contents
    Cannot raise an exception
    """
    results = []

    for sectionRenderer in contents:
        try:
            if "videoRenderer" in sectionRenderer:
                video_renderer = sectionRenderer["videoRenderer"]
                results.append(
                    Video(
                        video_renderer["videoId"],
                        video_renderer["title"]["runs"][0]["text"],
                        video_renderer["ownerText"]["runs"][0]["text"],
                        video_renderer["lengthText"]["simpleText"],
                        video_renderer["viewCountText"]["simpleText"],
                        video_renderer["publishedTimeText"]["simpleText"],
                        video_renderer["thumbnail"]["thumbnails"][-1]["url"], # best quality
                        video_renderer["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][0]["url"],
                        video_renderer["detailedMetadataSnippets"][0]["snippetText"]["runs"][0]["text"],
                        video_renderer.get("ownerBadges", [{}])[0].get("metadataBadgeRenderer", {}).get("style", "regular")
                    )
                )

            elif "channelRenderer" in sectionRenderer:
                channel_renderer = sectionRenderer["channelRenderer"]
                results.append(
                    Channel(
                        channel_renderer["channelId"],
                        channel_renderer["title"]["simpleText"],
                        channel_renderer["videoCountText"]["accessibility"]["accessibilityData"]["label"],
                        channel_renderer["thumbnail"]["thumbnails"][0]["url"], # starts with //
                        channel_renderer.get("ownerBadges", [{}])[0].get("metadataBadgeRenderer", {}).get("style", "regular")
                    )
                )
        except:
            continue

    return results

def youtube_search_parse(data: dict) -> dict[str, Any]:
    """ YouTube search default (and single for now) parsing method """
    result = {}

    try:
        result["estimated_results"] = data["estimatedResults"]
        contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
        result["results"] = youtube_search_contents_parse(contents[0]["itemSectionRenderer"]["contents"])
        result["_continuation"] = contents[1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
    except KeyError:
        raise ParserError("Parsing entities error\nProbably this because of YouTube updated their endpoints")

    return result

def youtube_search_continuation_parse(data: dict) -> dict[str, Any]:
    result = {}

    try:
        result["estimated_results"] = data["estimatedResults"]
        result["results"] = youtube_search_contents_parse(data["onResponseReceivedCommands"][0]["appendContinuationItemsAction"]["continuationItems"][0]["itemSectionRenderer"]["contents"])
        result["_continuation"] = data["onResponseReceivedCommands"][0]["appendContinuationItemsAction"]["continuationItems"][1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
    except KeyError:
        raise ParserError("Parsing entities error\nProbably this because of YouTube updated their endpoints")

    return result

def youtube_channel_parse(data: dict) -> dict[str, Any]:
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
    except KeyError:
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

        # parse icons
        try:
            link_icons: list[LinkIcon] = []
            for link in metadata["links"]:
                icons: dict[str, str] = {}
                for source in link["channelExternalLinkViewModel"]["favicon"]["sources"]:
                    icons[f"{source['width']}x{source['height']}"] = source["url"]
                link_icons.append(
                    LinkIcon(
                        link["channelExternalLinkViewModel"]["title"]["content"],
                        link["channelExternalLinkViewModel"]["link"]["content"],
                        icons
                    )
                )
        except KeyError:
            link_icons = None

        return ChannelDescription(
            metadata.get("description", None),
            metadata["joinedDateText"]["content"],
            metadata.get("country", None),
            link_icons
        )
    except:
       raise ParserError(f"Channel full description parsing failed\nProbably this because YouTube changed their data endpoints")