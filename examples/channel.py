"""
Get channel info API usage example
"""

from youtube_browsing_api import GetChannelInfo

try:
    chan = GetChannelInfo("UC_aEa8K-EOJ3D6gOs7HcyNg")
except Exception as e:
    print("Cannot fetch channel info :(")
    print(f"Reason:\n{e}")

if chan:
    print(f"Title              : {chan.title}")
    print(f"Subscribers count  : {chan.subs_count}")
    print(f"Thumbnail url      : {chan.thumbnail}")
    print(f"Banner url         : {chan.banner_img or 'no banner'}")
    print(f"Channel url        : {chan.channel_url}")
    print(f"Channel ID         : {chan.channel_id}")
    print(f"Vanity channel URL : {chan.vanity_channel_url}")
    print(f"Channel keywords   : {chan.keywords}")
    print(f"Short description  : {chan.short_desc}")
    print(f"Description        : {chan.desc}")

# get full channel description (send additional POST request)

try:
    chan.fetch_description()
    print(chan.full_desc.text)      # Channel's full description
    print(chan.full_desc.join_date) # Channel's join date
    print(chan.full_desc.region)    # Channel's region
except Exception as e:
    print("Cannot fetch channel's description :(")
    print(f"Reason:\n{e}")