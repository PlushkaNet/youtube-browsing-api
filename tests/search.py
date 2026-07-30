"""File with code for testing search functions"""

from time import sleep
from youtube_browsing_api import Search, Video, Channel

def check_results_type(results: list):
    for i in results:
        assert isinstance(i, Channel | Video)

def test_search(query: str, **kwargs):
    search = Search(query, **kwargs)
    search.as_list() # checks that converts successfully
    check_results_type(search.results)

    if len(search.results) == 0:
        print(f"WARNING: there are 0 results by query: {query}")
    
    search.next()
    check_results_type(search.results)

    if len(search.results) == 0:
        print(f"WARNING: there are 0 results after 1 search.next()")
    
    search.next()
    check_results_type(search.results)

    if len(search.results) == 0:
        print(f"WARNING: there are 0 results after 2 search.next()")

    print("test passed")

test_set = [
    "ncs songs", "no copyright music", "jawed", "i at the zoo", "Linus Tech Tips",
    "kasdlsajdkasjfksafhuagkjshdkfsdgtyfkjbdsgfkgrshalkdnfjhzdkhkxcnzkgiuahdkuhfiuryoiLJFLKD" # some unsearchable content
]

for query in test_set:
    test_search(query)
    sleep(0.5) # suspend a little to avoid be suspected by YouTube

print("search tests passed")