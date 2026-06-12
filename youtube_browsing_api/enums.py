from typing import Final

# TODO add more languages
class Languages:
    """ Enum with YouTube-supported localisations """
    EN    :Final[str] = "en"    # English
    AR    :Final[str] = "ar"    # Arabic
    ES_US :Final[str] = "es-us" # Spanish
    FR    :Final[str] = "fr"    # French
    DE    :Final[str] = "de"    # German
    AF    :Final[str] = "af"    # African
    PT    :Final[str] = "pt-pt" # Portuguese
    MN    :Final[str] = "mn"    # Mongolian
    RU    :Final[str] = "ru"    # Russian
    UK    :Final[str] = "uk"    # Ukrainian
    BE    :Final[str] = "be"    # Belarusian
    SR    :Final[str] = "sr"    # Serbian
    NL    :Final[str] = "nl"    # Dutch
    TR    :Final[str] = "tr"    # Turkish

# TODO add more regions
class Regions:
    """ Class serving YouTube-supported regions """
    US :Final[str] = "US" # United States
    GB :Final[str] = "GB" # United Kingdom
    AR :Final[str] = "AR" # Argentina
    AM :Final[str] = "AM" # Armenia
    AU :Final[str] = "AU" # Australia
    AT :Final[str] = "AT" # Austria
    AZ :Final[str] = "AZ" # Azerbaijan
    BY :Final[str] = "BY" # Belarus
    BR :Final[str] = "BR" # Brazil
    CA :Final[str] = "CA" # Canada
    CL :Final[str] = "CL" # Chile
    FR :Final[str] = "FR" # France
    DE :Final[str] = "DE" # Germany
    EG :Final[str] = "EG" # Egypt
    IN :Final[str] = "IN" # India
    JP :Final[str] = "JP" # Japan
    IT :Final[str] = "IT" # Italy
    RU :Final[str] = "RU" # Russia
    KZ :Final[str] = "KZ" # Kazakhstan
    UA :Final[str] = "UA" # Ukraine
    AE :Final[str] = "AE" # United Arab Imirates
    ES :Final[str] = "ES" # Spain

class AccountTypes:
    """ Enum with account types for channels """
    REGULAR  :Final[str] = "regular"  # just regular account type
    ARTIST   :Final[str] = "artist"   # verified music artist
    VERIFIED :Final[str] = "verified" # verified account type