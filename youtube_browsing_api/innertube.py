# pylint: disable=C0301
"""
File containing code for interaction with InnerTube API
"""

import json
import requests
from requests.cookies import CookieJar
from .enums import Languages, Regions
from .types import InvalidStatusError, JSONParsingError

# default Innertube client data template
WEB_CLIENT_NO_DATA = {
    "context": {
        "client": {
            "browserName": "Chrome",
            "browserVersion": "148.0.0.0",
            "clientFormFactor": "UNKNOWN_FORM_FACTOR",
            "clientName": "WEB",
            "clientVersion": "2.20260606.02.00", # some client
        },
        "request": {
            "useSsl": True
        }
    }
}

class InnertubeRequest:
    """
    Class containing code for manipulating request to InnerTube API v1 (youtubei/v1)
    """

    def __init__(self, endpoint: str, template: dict, timeout: float, cookies: CookieJar):
        """ Constructs class object"""
        self._endpoint = endpoint
        self._body = template
        self._timeout = timeout
        self.cookies = cookies # cookies can be replaced by new response's cookies in .send() method

    def __setitem__(self, k: str, v):
        """ Just interface for dictionary's method __setitem__ inside class object """
        self._body[k] = v

    def __getitem__(self, k: str):
        """ Just interface for dictionary's method __getitem__ inside class object """
        return self._body[k]

    def perform(self) -> dict:
        """
        Performes a request to InnerTube API
        Returns JSON data from YouTube on success
        Raises an exception on failure

        This method will fresh up cookies
        """
        response = requests.post(
            "https://www.youtube.com/youtubei/v1/" + self._endpoint + "?prettyPrint=false",
            json=self._body,
            timeout=self._timeout,
            cookies=self.cookies
        )

        if response.status_code != 200:
            raise InvalidStatusError(response.status_code)

        self.cookies = response.cookies # freshes up cookies

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise JSONParsingError("Failed to parse JSON from YouTube's InnerTube API\nProbably this happens because YouTube returned invalid JSON content") from e

        return data

class Innertube:
    """
    Class containing code for serving request settings
    """

    def __init__(self, hl: str = Languages.EN, gl: str = Regions.US, template: dict = WEB_CLIENT_NO_DATA, timeout: float = 5.0):
        """
        Constructs Innertube client with passed arguments
        Fields:
        - hl       # language, default = "en"
        - gl       # region, default = "US"
        - template # request's body template, default = WEB_CLIENT_NO_DATA
        - timeout  # all subrequests timeout, default = 5.0
        """
        self._template = template
        self._template["context"]["gl"] = gl # sets up region in template context
        self._template["context"]["hl"] = hl # sets up language in template context
        self._timeout = timeout # timeout for all requests maked by Innertube

        self.cookies = requests.cookies.CookieJar() # creates empty CookieJar

    def make_request(self, endpoint: str) -> InnertubeRequest:
        """ Constructs InnertubeRequest object and returns it """
        return InnertubeRequest(endpoint, self._template, self._timeout, self.cookies)
