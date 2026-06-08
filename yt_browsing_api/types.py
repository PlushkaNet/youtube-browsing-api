from dataclasses import dataclass, asdict

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

    def as_dict(self):
        """ Returns Video as a JSON-like object """
        return asdict(self)


@dataclass
class Channel:
    id           :str
    title        :str
    subs_count   :str
    thumbnail    :str
    account_type :str

    def as_dict(self):
        """ Returns Channel as a JSON-like object """
        return asdict(self)