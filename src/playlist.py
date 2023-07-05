import json

import isodate

from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist = youtube.playlistItems().list(playlistId=playlist_id,
                                                part='contentDetails, snippet'
                                                ).execute()
        # print(json.dumps(playlist, indent=2, ensure_ascii=False))
        self.playlist_id = playlist_id
        self.title = playlist['items'][0]['snippet']['title'][:24]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self):
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total = isodate.parse_duration("PT0M0S")
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        max_likes = 0
        for video in video_response['items']:
            if max_likes < int(video['statistics']['likeCount']):
                max_likes = int(video['statistics']['likeCount'])
                max_likes_video = video['id']
        return "https://youtu.be/" + max_likes_video
