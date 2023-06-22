import json
import os
from googleapiclient.discovery import build

api_key = os.getenv('GOOGLE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        data = youtube.channels().list(id=channel, part='snippet,statistics').execute()

        self.__channel_id = data['items'][0]['id']
        self.title = data['items'][0]['snippet']['title']
        self.description = data['items'][0]['snippet']['description']
        self.url = data['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = data['items'][0]['statistics']['subscriberCount']
        self.video_count = data['items'][0]['statistics']['videoCount']
        self.view_count = data['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, json_file):
        dict_ = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(json_file, 'w') as file:
            file.write(json.dumps(dict_, indent=2, ensure_ascii=False))
