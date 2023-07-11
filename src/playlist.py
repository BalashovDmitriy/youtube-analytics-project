import datetime

import isodate

from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist = youtube.playlists().list(id=playlist_id,
                                            part='contentDetails, snippet').execute()['items'][0]['snippet']
        playlist_items = youtube.playlistItems().list(playlistId=playlist_id,
                                                      part='contentDetails, snippet'
                                                      ).execute()['items']
        video_ids = [video['contentDetails']['videoId'] for video in playlist_items]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()['items']
        self.title = playlist['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self):
        temp = [item['contentDetails']['duration'] for item in self.video_response]
        time_delta_sec = sum([isodate.parse_duration(elem).seconds for elem in temp])
        return datetime.timedelta(seconds=time_delta_sec)

    def show_best_video(self):
        max_likes = max([int(item['statistics']['likeCount']) for item in self.video_response])
        max_likes_video = [video['id'] for video in self.video_response if
                           video['statistics']['likeCount'] == str(max_likes)][0]
        return "https://youtu.be/" + max_likes_video
