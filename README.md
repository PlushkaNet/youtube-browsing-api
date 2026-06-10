<center><h2>Youtube browsing API</h2></center>

## Quick start
Install stable package version via pip using:
```
pip install git+https://github.com/PlushkaNet/youtube_browsing_api.git
```

Or try nightly using:
```
pip install git+https://github.com/PlushkaNet/youtube_browsing_api@dev
```

<b>Suggestion queries usage example:</b>
```
from yt_browsing_api import get_suggest_queries

queries: list[str] | None = get_suggest_queries("NCS")

for i in range(len(queries)):
    print(f"Suggestion query #{i+1}: {queries[i]}")
```

<b>Search usage example:</b>
```
from yt_browsing_api import Search

results = search("NCS", page=1)

print(results.found)   # prints how much entries are there
print(results.results) # list of videos and channels
```

<h3>Complete examples can be found in <a href="examples/">examples/</a> directory</h3>
<ul>
<li><b><a href="examples/suggestion_queries.py">Suggestion queries complete example</a></b></li>
<li><b><a href="examples/search.py">Videos/Channels search complete example</a></b></li>
<li><b><a href="examples/channel.py">Fetching channel info complete example</a></b></li>
</ul>

<b>Currently supports:</b>
- Suggestion queries
- Search
- Exploring channels (partly)

<b>In development (channels):</b>
- Recent videos
- All videos
- Playlists
- External platforms links in description support

<b>In development (search) </b>
- .next() method (to fetch results from next page automatically)