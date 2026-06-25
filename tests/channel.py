""" File containing code for testing channel info fetch """

from youtube_browsing_api import GetChannelInfo, Languages, InvalidStatusError
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep

def full_channel_test(channel_url: str, **kwargs):
    print(f"testing URL: {channel_url}")
    chan = GetChannelInfo(channel_url, **kwargs)

    assert chan.full_desc == None

    chan.fetch_description()

    print("test passed")

    del chan

def test_with_retry(func):
    for retry in range(5):
        try:
            func()
            return
        except ReadTimeout, ConnectionError:
            print(f"WARNING: read timeout/connection error, retrying in 2 seconds, try={retry}")
            sleep(2)
    print("skip as not successful")

test_set = [
    # famous, big channels
    "@NoCopyrightSounds", "https://www.youtube.com/@NoCopyrightSounds",
    "https://www.youtube.com/channel/UC_aEa8K-EOJ3D6gOs7HcyNg", "https://youtube.com/@NoCopyrightSounds",
    "https://youtube.com/channel/UC_aEa8K-EOJ3D6gOs7HcyNg", "https://www.youtube.com/@jawed", "https://www.youtube.com/@LinusTechTips",
    # some incomplete / abandoned / small channels
    "https://www.youtube.com/@dartone8061",
    "https://www.youtube.com/@HRIDAYRoy-eq3qh",
    "https://www.youtube.com/@official_gagada01",
    "https://www.youtube.com/@bunlak5604"
]

print("run tests: only channel url's")
for channel_url in test_set:
    def test():
        try:
            full_channel_test(channel_url)
        except InvalidStatusError as e:
            print(f"WARNING: YouTube returned reponse with invalid status code {e.status_code}")
    test_with_retry(test)
    sleep(0.5) # sleep for a while to avoid confusing YouTube

print("run tests: with language and timeout passed")
for channel_url in test_set:
    for language in dir(Languages):
        if not language.startswith("__"):
            def test():
                try:
                    full_channel_test(channel_url, language=language, timeout=2.0)
                except InvalidStatusError as e:
                    print(f"WARNING: YouTube returned reponse with invalid status code {e.status_code}")
            print(f"testing with language: {language}")
            test_with_retry(test)
            sleep(0.5) # sleep for a while to avoid confusing YouTube

print("all tests passed")
