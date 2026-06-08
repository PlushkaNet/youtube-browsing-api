from dataclasses import dataclass

@dataclass
class Video:
    id                :str
    title             :str
    author            :str
    duration          :str
    views             :str
    publish_time      :str
    video_thumbnail   :str
    channel_thumbnail :str
    short_desc        :str
    account_type      :str


@dataclass
class Channel:
    id           :str
    title        :str
    subs_count   :str
    thumbnail    :str
    account_type :str