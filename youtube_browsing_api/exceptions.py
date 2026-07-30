"""File containing code for common exceptions"""

class YouTubeError(Exception):
    """Base class for all YouTube exceptions"""

class InnerTubeAPIRequestError(YouTubeError):
    """Raised when cannot perform a request to InnerTube API"""

class ExtractorError(YouTubeError):
    """Raised when cannot extract data from page"""

class ParserError(YouTubeError):
    """Raised when cannot parse response from YouTube due to unexpected content"""

class JSONParsingError(YouTubeError):
    """Raised when cannt parse JSON from YouTube"""

class InvalidStatusError(YouTubeError):
    """Raised when InnerTube API returned response with unexpected status"""
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Status code is {status_code}")
