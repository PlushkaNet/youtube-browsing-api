"""
Search API usage example
"""

from yt_browsing_api import Search, Video, Channel, Languages, Regions

try:
    results = Search("NCS")
except Exception as e:
    results = None
    print("An error occured while trying to search :(")
    print(f"An error: {e}")

def pretty_print_result(result: Video | Channel):
    if isinstance(i, Channel):
        print(f"Channel:")

        print(f"\tTitle:        {i.title}")        # Channel's title
        print(f"\tID:           {i.id}")           # Channel's ID
        print(f"\tAccount type: {i.account_type}") # Channel's account type
        print(f"\tSubs count:   {i.subs_count}")   # Channel's subscritbers count
        print(f"\tThumb url:    {i.thumbnail}")    # Channel's thumbnail URL

    elif isinstance(i, Video):
        print(f"Video:")

        print(f"\tTitle:         {i.title}")             # Video's title
        print(f"\tID:            {i.id}")                # Video's ID
        print(f"\tAuthor:        {i.author}")            # Video's author (channel)
        print(f"\tAccount type:  {i.account_type}")      # Video's author account type
        print(f"\tDuration:      {i.duration}")          # Video's duration
        print(f"\tPublish time:  {i.publish_time}")      # Video's publish time
        print(f"\tViews count:   {i.views}")             # Video's views count
        print(f"\tShort desc:    {i.short_desc}")        # Video's short description (first part of full description)
        print(f"\tVideo thumb:   {i.video_thumbnail}")   # Video's thumbnail URL (in highest quality)
        print(f"\tChannel thumb: {i.channel_thumbnail}") # Video's author's (channel's) thumbnail URL

if results:
    # prints all results
    for i in results:
        pretty_print_result(i)


# you also can search videos in specific region with specific language chosen
try:
    # searching with French language in French region
    results = Search("NCS", language=Languages.FR, region=Regions.FR)
except Exception as e:
    results = None
    print("An error occured while trying to search :(")
    print(f"An error: {e}")