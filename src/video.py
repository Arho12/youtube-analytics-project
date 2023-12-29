import os
from googleapiclient.discovery import build


class Video:
    YT_API_KEY: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        self.video_id = video_id
        try:
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=video_id
                                                              ).execute()

            self.title = video_response["items"][0]["snippet"]["title"]
            self.url = f'https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A{self.video_id}'
            self.view_count = video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = video_response["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.title = None
            self.like_count = None
            self.view_count = None

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.YT_API_KEY)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
