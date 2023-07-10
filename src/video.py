from src.channel import Channel


class Video:
    def __init__(self, video_id):
        youtube = Channel.get_service()
        try:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            self.video_id = video_id
            self.title = video_response['items'][0]['snippet']['title']
            self.url = "https://www.youtube.com/watch?v=" + video_id
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist):
        super().__init__(video_id)
        self.playlist = playlist
