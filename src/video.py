from src.channel import Channel


class Video:
    def __init__(self, id_):
        youtube = Channel.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=id_
                                               ).execute()
        self.id_ = id_
        self.name = video_response['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/watch?v=" + id_
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name


class PLVideo(Video):

    def __init__(self, id_, playlist):
        super().__init__(id_)
        self.playlist = playlist
