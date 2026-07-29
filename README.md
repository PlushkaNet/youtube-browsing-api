# 🔎 Youtube browsing API

> *Uses both document parsing and InnerTube API to fetch data from YouTube*

## 🔥 Quick start

Install stable package version via pip using:
```
pip install git+https://github.com/PlushkaNet/youtube_browsing_api.git
```

Or try nightly using:
```
pip install git+https://github.com/PlushkaNet/youtube_browsing_api@dev
```

## ⚙️ Usage

**📜 Suggestion queries usage example**
```
from youtube_browsing_api import get_suggest_queries

queries: list[str] | None = get_suggest_queries("NCS")

for i in range(len(queries)):
    print(f"Suggestion query #{i+1}: {queries[i]}")
```

**🔎 Search usage example:**
```
from youtube_browsing_api import Search

results = search("NCS")

print(results.found)   # prints how much entries are there
print(results.results) # list of videos and channels

results.next() # fetch next results

print(results.results) # new results
```

**🔎 Exploring channels usage example:**
```
from youtube_browsing_api import GetChannelInfo

chan = GetChannelInfo("NoCopyrightSounds")

print(chan.title)
print(chan.subs_count)
print(chan.thumbnail) # thumbnail URL
print(chan.banner_img) # can be None

chan.fetch_description()

print(chan.full_desc.text)
print(chan.full_desc.join_date)
print(chan.full_desc.region)
```

**📚 Complete examples can be found in [examples/](examples/) directory**
- **[Suggestion queries complete example](examples/suggestion_queries.py)**
- **[Videos/Channels search complete example](examples/search.py)**
- **[Fetching channel info complete example](examples/channel.py)**

**✅ Currently supports:**
- Suggestion queries
- Search
- Exploring channels (partly)

**🛠️ In development (channels):**
- Recent videos
- All videos
- Playlists

**🛠️ In development (search):**
- Search filters

**🛠️ In development (internal):**
- Increase persistence of parsers

---

*If you find this project helpful, please consider giving it a ⭐*