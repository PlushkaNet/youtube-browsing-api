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

<b>Currently supports:</b>
- Suggestion queries

<b>In development:</b>
- Search
- Exploring channels