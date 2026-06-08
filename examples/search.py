"""
Search API usage example
"""

from yt_browsing_api import search, Video, Channel, Languages, Regions

results: list[Channel | Video] | None = search("NCS")

for i in results:
    if type(i) == Channel:
        print(f"Channel:")

        print(f"\tTitle:        {i.title}")        # Channel's title
        print(f"\tID:           {i.id}")           # Channel's ID
        print(f"\tAccount type: {i.account_type}") # Channel's account type
        print(f"\tSubs count:   {i.subs_count}")   # Channel's subscritbers count
        print(f"\tThumb url:    {i.thumbnail}")    # Channel's thumbnail URL

    elif type(i) == Video:
        print(f"Video:")

        print(f"\tTitle:         {i.title}")             # Video's title
        print(f"\tID:            {i.id}")                # Video's ID
        print(f"\tAuthor:        {i.author}")            # Video's author (channel)
        print(f"\tAccount type:  {i.account_type}")      # Video's author account type
        print(f"\tDuration:      {i.duration}")          # Video's duration
        print(f"\tPublish time:  {i.publish_time}")      # Video's publish time
        print(f"\tViews count:   {i.views}")             # Video's views count
        print(f"\tShort desc:    {i.short_desc}")        # Video's short description (part of full description)
        print(f"\tVideo thumb:   {i.video_thumbnail}")   # Video's thumbnail URL (high quality)
        print(f"\tChannel thumb: {i.channel_thumbnail}") # Video's author's (channel's) thumbnail URL

# you also can search videos in specific region with specific language chosen
results: list[Channel | Video] | None = search("NCS", language=Languages.FR, region=Regions.FR, page=2)