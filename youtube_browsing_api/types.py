""" File containing code for common exceptions and YouTube entries objects """

from dataclasses import dataclass, asdict
from .enums import AccountTypes

class ExtractorError(Exception):
    pass


class ParserError(Exception):
    pass


class JSONParsingError(Exception):
    pass


class InvalidStatusError(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Status code is {status_code}")


def _translate_account_type(account_type: str) -> str:
    """ Translates account type to internal StrEnum type """
    if account_type == "BADGE_STYLE_TYPE_VERIFIED_ARTIST":
        account_type = AccountTypes.ARTIST
    elif account_type == "BADGE_STYLE_TYPE_VERIFIED":
        account_type = AccountTypes.VERIFIED
    else:
        account_type = AccountTypes.REGULAR
    
    return account_type


class Video:
    """
    Class representing a YouTube video
    Fields:
    - id                  # YouTube video's ID                                 (str)
    - title               # YouTube video's title                              (str)
    - author              # YouTube video's author (channel)                   (str)
    - duration            # YouTube video's duration in seconds                (int)
    - views               # YouTube video's views count                        (int)
    - publish_time        # YouTube video's publish time                       (str)
    - video_thumbnail     # YouTube video's high quality thumbnail url         (str)
    - channel_thumbnail   # YouTube video's author's (channel's) thumbnail url (str)
    - short_desc          # YouTube video's short description                  (str)
    - account_type        # YouTube video's author's (channel's) account type  (str)
    """

    __slots__ = ["id", "title", "author", "duration", "views", "publish_time", "video_thumbnail", "channel_thumbnail", "short_desc", "account_type"]
    
    def __init__(
         self, id: str, title: str, author: str, duration: str,
         views: str, publish_time: str, video_thumbnail: str,
         channel_thumbnail: str, short_desc: str, account_type: str
        ):
        """
        Creates Video object

        Next fields may be converted:
        - account_type -> AccountTypes
        - views        -> int
        - duration     -> int, in seconds
        """

        self.id                = id
        self.title             = title
        self.author            = author
        self.publish_time      = publish_time
        self.video_thumbnail   = video_thumbnail
        self.channel_thumbnail = channel_thumbnail
        self.short_desc        = short_desc
        self.account_type      = _translate_account_type(account_type)
        
        # translating duration field (str) to int (seconds)
        # its often looks like
        # 3:21:53, not more than 3 parts, and not less than 2 parts
        timeparts = duration.split(":")
        try:
            if len(timeparts) == 2:
                self.duration = int(timeparts[0])*60+int(timeparts[1])
            elif len(timeparts) == 3:
                self.duration = int(timeparts[0])*60*60+int(timeparts[1])*60+int(timeparts[2])
        except:
            self.duration = duration # fallback

        # translating views field
        # its often looks like
        # 1,234,567 views
        # or 1,128 views
        # or 120 views
        # so we just remove commas
        try:
            views_num_str = views.split()[0] # should be list of 2 items
            self.views = str(int(views_num_str.replace(",", "")))
        except:
            self.views = views # fallback

    def as_dict(self):
        """ Returns Video as a JSON-like object """
        return {
            "id"                :self.id,
            "title"             :self.title,
            "author"            :self.author,
            "duration"          :self.duration,
            "views"             :self.views,
            "publish_time"      :self.publish_time,
            "video_thumbnail"   :self.video_thumbnail,
            "channel_thumbnail" :self.channel_thumbnail,
            "short_desc"        :self.short_desc,
            "account_type"      :self.account_type
        }

    def __repr__(self):
        return "Video("                                                 \
            +"id"                + "='" +self.id                + "'"   \
            +"title"             + "='" +self.title             + "', " \
            +"author"            + "='" +self.author            + "', " \
            +"duration"          + "="  +str(self.duration)     + ", "  \
            +"views"             + "="  +str(self.views)        + ", "  \
            +"publish_time"      + "='" +self.publish_time      + "', " \
            +"video_thumbnail"   + "='" +self.video_thumbnail   + "', " \
            +"channel_thumbnail" + "='" +self.channel_thumbnail + "', " \
            +"short_desc"        + "='" +self.short_desc        + "', " \
            +"account_type"      + "='" +self.account_type      + "'"   \
            +")"


@dataclass
class Channel:
    id           :str
    title        :str
    subs_count   :str
    thumbnail    :str
    account_type :str

    def __post_init__(self):
        self.account_type = _translate_account_type(self.account_type)
        
        if self.thumbnail.startswith("//"):
            self.thumbnail = "https:" + self.thumbnail

    def as_dict(self):
        """ Returns Channel as a JSON-like object """
        return asdict(self)


@dataclass
class ChannelDescription:
    """
    Class representing channel's description
    """
    text      :str
    join_date :str
    region    :str
    # urls to be added here

    def as_dict(self):
        """ Returns ChannelDescription as a JSON-like object """
        return asdict(self)