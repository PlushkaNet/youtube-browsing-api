""" File containing code for testing search functions """

from typing import Union
from youtube_browsing_api import Search, SearchFromDocument, Video, Channel, Languages, Regions
from time import sleep
from youtube_browsing_api.innertube import Innertube

def check_results_type(results: list):
    for i in results:
        assert isinstance(i, Union[Channel, Video])

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

print("all tests passed")

# TODO add SearchFromDocument tests
# TODO add tests with different languages and regions
