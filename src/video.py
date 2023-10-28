import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        try:
            self._video_id = video_id
            self._youtube = self.get_service()
            self.title = self._youtube['items'][0]['snippet']['title']
            self.url = self._youtube['items'][0]['id']
            self.view_count = self._youtube['items'][0]['statistics']['viewCount']
            self.like_count = self._youtube['items'][0]['statistics']['likeCount']
            if not self._youtube:
                raise IndexError(self._youtube)
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def get_service(self):
        youtube = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self._video_id
                                               ).execute()
        return video_response

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
