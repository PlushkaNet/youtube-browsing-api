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
    US :Final[str] = "us" # United States
    GB :Final[str] = "gb" # United Kingdom
    AR :Final[str] = "ar" # Argentina
    AM :Final[str] = "am" # Armenia
    AU :Final[str] = "au" # Australia
    AT :Final[str] = "at" # Austria
    AZ :Final[str] = "az" # Azerbaijan
    BY :Final[str] = "by" # Belarus
    BR :Final[str] = "br" # Brazil
    CA :Final[str] = "ca" # Canada
    CL :Final[str] = "cl" # Chile
    FR :Final[str] = "fr" # France
    DE :Final[str] = "de" # Germany
    EG :Final[str] = "eg" # Egypt
    IN :Final[str] = "in" # India
    JP :Final[str] = "jp" # Japan
    IT :Final[str] = "it" # Italy
    RU :Final[str] = "ru" # Russia
    KZ :Final[str] = "kz" # Kazakhstan
    UA :Final[str] = "ua" # Ukraine
    AE :Final[str] = "ae" # United Arab Imirates
    ES :Final[str] = "es" # Spain

class AccountTypes:
    """ Enum with account types for channels """
    REGULAR  :Final[str] = "regular"  # just regular account type
    ARTIST   :Final[str] = "artist"   # verified music artist
    VERIFIED :Final[str] = "verified" # verified account type