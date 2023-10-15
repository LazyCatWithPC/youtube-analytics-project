from googleapiclient.discovery import build
import json
import os


class Channel:
    """Класс для ютуб-канала"""
    # Программа не видела переменную среды, так что пришлось добавить в PyCharm

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.channel_info = self.get_service().channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.video_count = self.channel_info["items"][0]["statistics"]["videoCount"]
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.description = self.channel_info["items"][0]["snippet"]["description"]
        self.channel_subscribers = int(self.channel_info["items"][0]["statistics"]["subscriberCount"])
        self.channel_views = self.channel_info["items"][0]["statistics"]["viewCount"]

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        return self.channel_subscribers + other.channel_subscribers

    def __sub__(self, other):
        return self.channel_subscribers - other.channel_subscribers

    def __gt__(self, other):
        return self.channel_subscribers > other.channel_subscribers

    def __ge__(self, other):
        return self.channel_subscribers >= other.channel_subscribers

    def __eq__(self, other):
        return self.channel_subscribers == other.channel_subscribers

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        youtube = build("youtube", "v3", developerKey=os.getenv("API_KEY"))
        return youtube

    def to_json(self, json_name):
        data = {"channel_id": self.__channel_id,
                "channel_title": self.title,
                "description": self.description,
                "channel_url": self.url,
                "subscribers_count": self.channel_subscribers,
                "video_count": self.video_count,
                "views": self.channel_views}
        with open(json_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
