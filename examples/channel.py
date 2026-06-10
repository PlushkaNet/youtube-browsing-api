"""
Get channel info API usage example
"""

from yt_browsing_api import GetChannelInfo

try:
    chan = GetChannelInfo("NoCopyrightSounds")
except Exception as e:
    print("Cannot fetch channel info :(")
    print(f"Reason:\n{e}")

if chan:
    print(f"Title              : {chan.title}")
    print(f"Subscribers count  : {chan.subs_count}")
    print(f"Thumbnail url      : {chan.thumbnail}")
    print(f"Banner url         : {chan.banner_img | 'no banner'}")

# get channel description (send addition POST request)

try:
    chan.fetch_description()
except Exception as e:
    print("Cannot fetch channel's description :(")
    print(f"Reason:\n{e}")

print(chan.desc.text)      # Channel's full description
print(chan.desc.join_date) # Channel's join date
print(chan.desc.region)    # Channel's region