from yt_browsing_api import get_suggest_queries

queries: list[str] | None = get_suggest_queries("NCS")

for i in range(len(queries)):
    print(f"Suggestion query #{i+1}: {queries[i]}")


from yt_browsing_api import Languages, Regions

# suggest queries from France with Turkish localization
queries: list[str] | None = get_suggest_queries("NCS", language=Languages.TR, region=Regions.FR)

for i in range(len(queries)):
    print(f"Suggestion query #{i+1}: {queries[i]}")