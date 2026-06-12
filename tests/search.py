""" File containing code for testing search functions """

from youtube_browsing_api import Search, SearchFromDocument, Video, Channel, Languages, Regions
from youtube_browsing_api.innertube import Innertube

# InnerTube search
search = Search("NCS")

search.as_list() # checking that works correctly by calling .as_list() convertion
assert search.found != None
assert isinstance(search.results, list)

if len(search.results) == 0:
    print("WARNING: 0 results for test #1")

for i in search:
    if type(i) not in [Channel, Video]:
        raise Exception("Search.__iter__ failed: i is not instance of Video or Channel")

assert isinstance(search._innertube, Innertube)

# InnerTube search with special flags
search = Search("NCS", language=Languages.AF, region=Regions.IN, timeout=9.0)

search.as_list() # checking that works correctly by calling .as_list() convertion
assert search.found != None
assert isinstance(search.results, list)

if len(search.results) == 0:
    print("WARNING: 0 results for test #2")

for i in search:
    if type(i) not in [Channel, Video]:
        raise Exception("Search.__iter__ failed: i is not instance of Video or Channel")

assert isinstance(search._innertube, Innertube)

# Parsing search
search = SearchFromDocument("NCS")

search.as_list()
assert search.found != None
assert isinstance(search.results, list)

if len(search.results) == 0:
    print("WARNING: 0 results for test #3")

for i in search:
    if type(i) not in [Channel, Video]:
        raise Exception("SearchFromDocument.__iter__ failed: i is not instance of Video or Channel")

# Parsing search with special flags

spec_timeout = 9.0
search = SearchFromDocument("NCS", language=Languages.AF, region=Regions.IN, timeout=spec_timeout)

search.as_list()
assert search.found != None
assert isinstance(search.results, list)
assert search._timeout == spec_timeout

if len(search.results) == 0:
    print("WARNING: 0 results for test #4")

for i in search:
    if type(i) not in [Channel, Video]:
        raise Exception("SearchFromDocument.__iter__ failed: i is not instance of Video or Channel")

print("All tests passed successfully!")