from typing import Union, Optional
from .types import Video, Channel
from .enums import AccountTypes


def _translate_account_type(account_type: str) -> str:
    """ Translates account type to internal StrEnum type """
    if account_type == "BADGE_STYLE_TYPE_VERIFIED_ARTIST":
        account_type = AccountTypes.ARTIST
    elif account_type == "BADGE_STYLE_TYPE_VERIFIED":
        account_type = AccountTypes.VERIFIED
    else:
        account_type = AccountTypes.REGULAR
    
    return account_type


def beautify_Video(obj: Video):
    """
    Beautifies Video object
    Returns modified Video object or original Video object if failed

    Next fields may be translated:
    - account_type
    - views
    - duration
    """
    obj.account_type = _translate_account_type(obj.account_type)

    # translating views field
    # its often looks like
    # 1,234,567 views
    # or 1,128 views
    # or 120 views
    # so we just remove commas
    try:
        views_num_str = obj.views.split()[0] # should be list of 2 items
        obj.views = str(int(views_num_str.replace(",", "")))
    except: pass

    # translating duration field (str) to int (seconds)
    # its often looks like
    # 3:21:53, not more than 3 parts, and not less than 2 parts
    timeparts = obj.duration.split(":")
    try:
        if len(timeparts) == 2:
            obj.duration = int(timeparts[0])*60+int(timeparts[1])
        elif len(timeparts) == 3:
            obj.duration = int(timeparts[0])*60*60+int(timeparts[1])*60+int(timeparts[2])
    except: pass

    return obj


def beautify_Channel(obj: Channel) -> Channel:
    """
    Beautifies Channel object
    Returns modified Channel object or original Channel object if failed

    Next fields may be translated:
    - thumbnail
    - account_type
    """
    obj.account_type = _translate_account_type(obj.account_type)

    if obj.thumbnail.startswith("//"):
        obj.thumbnail = "https:" + obj.thumbnail

    return obj


def beautify(obj: Union[Video, Channel]) -> Union[Video, Channel]:
    """
    Beautifies Video or Channel object
    Translates different strings to numeric values and adds missed "https:"
    This method combines beautify_Channel and beautify_Video calls
    """
    if type(obj) == Video:
        return beautify_Video(obj)
    elif type(obj) == Channel:
        return beautify_Channel(obj)