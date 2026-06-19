# pylint: disable=C0301
"""
File containing code for parsing suggest queries from YouTube
"""

from typing import Optional, List
import json
from urllib import parse
import requests

from .enums import Languages, Regions

# clears google's response
def _clear_google_response(resp:str) -> str:
    return resp.removeprefix('window.google.ac.h(').removesuffix(')')

# parses only text queries
def parse_text_queries(text_json:str) -> Optional[List[str]]:
    try:
        data = json.loads(text_json)
    except json.JSONDecodeError:
        return None

    if type(data) != list or len(data) <= 1:
        return None

    combined_queries = data[1]
    if type(combined_queries) != list:
        return None # not a valid queries list

    queries: List[str] = []

    for i in combined_queries:
        if len(i) == 0: # skip empty sets
            continue
        if isinstance(i[0], str): # append only string queries
            queries.append(i[0])

    return queries

def get_suggest_queries(query: str, language=Languages.EN, region=Regions.US, timeout=5.0) -> Optional[List[str]]:
    """
    Get suggest queries from YouTube
    Arguments:
    - query       [required]
    - language    [optional], default = "en"
    - region      [optional], default = "us

    Returns List[str] with suggest queries on success
    Returns None if error occured
    """

    # gl - region
    # hl - language
    # cp - number of suggestions
    # q - query
    query = f"https://suggestqueries-clients6.youtube.com/complete/search?ds=yt&hl={language}&gl={region}&client=youtube&gs_ri=youtube&h=180&w=320&ytvs=1&gs_id=i&q={parse.quote(query, safe="")}"

    try:
        response = requests.get(query, timeout=timeout)
    except:
        return None

    if response.ok:
        return parse_text_queries(_clear_google_response(response.text))
    return None
