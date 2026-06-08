"""
Get channel info API usage example
"""

from yt_browsing_api import get_channel, ChannelInfo

chan: ChannelInfo | None = get_channel("NoCopyrightSounds")

if chan:
    print(f"Title              : {chan.title}")
    print(f"Subscribers count  : {chan.subs_count}")
    print(f"Thumbnail url      : {chan.thumbnail}")
    print(f"Banner url         : {chan.banner_img | 'no banner'}")