""" File containing code for testing channel info fetch """

from youtube_browsing_api import GetChannelInfo, Languages

chan_id = "UC_aEa8K-EOJ3D6gOs7HcyNg" # NCS channel

# basic test
chan = GetChannelInfo(chan_id)
test_i = 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with username
chan = GetChannelInfo("@NoCopyrightSounds")

test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with URL (vanity)
chan = GetChannelInfo("https://www.youtube.com/@NoCopyrightSounds")
test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with URL (standart)
chan = GetChannelInfo(f"https://www.youtube.com/channel/{chan_id}")
test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with no-www URL (vanity)
chan = GetChannelInfo("https://youtube.com/@NoCopyrightSounds")
test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with no-www URL (standart)
chan = GetChannelInfo(f"https://youtube.com/channel/{chan_id}")
test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

# test with special flags
chan = GetChannelInfo(chan_id, language=Languages.TR, timeout=9.0)
test_i += 1

assert chan.full_desc == None
if len(chan.short_desc) == 0:
    print(f"WARNING: short_desc for test #{test_i} is 0")

if chan.banner_img == None:
    print(f"WARNING: banner_img for test #{test_i} is None")

print("All tests passed successfully!")