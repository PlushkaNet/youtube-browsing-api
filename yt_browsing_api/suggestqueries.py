"""
Parsing suggest queries from YouTube
"""

from enum import Enum
from typing import Optional, List
import requests
import json

# TODO add more languages
class Languages(Enum):
    EN    = "en"    # English
    AR    = "ar"    # Arabic
    ES_US = "es-us" # Spanish
    FR    = "fr"    # French
    DE    = "de"    # German
    AF    = "af"    # African
    PT    = "pt-pt" # Portuguese
    MN    = "mn"    # Mongolian
    RU    = "ru"    # Russian
    UK    = "uk"    # Ukrainian
    BE    = "be"    # Belarusian
    SR    = "sr"    # Serbian
    NL    = "nl"    # Dutch
    TR    = "tr"    # Turkish

# TODO add more regions
class Regions(Enum):
    US = "us" # United States
    GB = "gb" # United Kingdom
    AR = "ar" # Argentina
    AM = "am" # Armenia
    AU = "au" # Australia
    AT = "at" # Austria
    AZ = "az" # Azerbaijan
    BY = "by" # Belarus
    BR = "br" # Brazil
    CA = "ca" # Canada
    CL = "cl" # Chile
    FR = "fr" # France
    DE = "de" # Germany
    EG = "eg" # Egypt
    IN = "in" # India
    JP = "jp" # Japan
    IT = "it" # Italy
    RU = "ru" # Russia
    KZ = "kz" # Kazakhstan
    UA = "ua" # Ukraine
    AE = "ae" # United Arab Imirates
    ES = "es" # Spain

# clears google's response
def clear_google_response(resp:str) -> str:
    return resp.removeprefix('window.google.ac.h(').removesuffix(')')


# parses only text queries
def parse_text_queries(text_json:str) -> Optional[List[str]]:
    try:
        data = json.loads(text_json)
    except:
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
        if type(i[0]) == str: # append only string queries
            queries.append(i[0])

    return queries


def get_suggest_queries(query: str, language=Languages.EN, region=Regions.US) -> Optional[List[str]]:
    """
    Get suggest queries from YouTube
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
    query = f"https://suggestqueries-clients6.youtube.com/complete/search?ds=yt&hl={language}&gl={region}&client=youtube&gs_ri=youtube&h=180&w=320&ytvs=1&gs_id=i&q={query}"

    try:
        response = requests.get(query, timeout=12.0)
    except:
        return None
    
    if response.ok:
        return parse_text_queries(clear_google_response(response.text))
    return None