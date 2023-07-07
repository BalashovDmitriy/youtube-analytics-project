import json

import isodate

from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='contentDetails, snippet'
                                                     ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        self.title = playlist['items'][0]['snippet']['title'][:24]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self):
        total = isodate.parse_duration("PT0M0S")
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        max_likes = 0
        for video in self.video_response['items']:
            if max_likes < int(video['statistics']['likeCount']):
                max_likes = int(video['statistics']['likeCount'])
                max_likes_video = video['id']
        return "https://youtu.be/" + max_likes_video
