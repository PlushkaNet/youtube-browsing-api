<center><h2>Youtube browsing API</h2></center>

## Quick start
Install package via pip using:
```
pip install git+https://github.com/PlushkaNet/youtube_browsing_api.git
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
from yt_browsing_api import search

results: list = search("NCS", page=1)

print(results)
```

<h3>Complete examples can be found in <a href="examples/">examples/</a> directory</h3>
<ul>
<li><b><a href="examples/suggestion_queries.py">Suggestion queries complete example</a></b></li>
<li><b><a href="examples/search.py">Videos/Channels search complete example</a></b></li>
</ul>

<b>Currently supports:</b>
- Suggestion queries
- Search

<b>In development:</b>
- Exploring channels