import urllib.request
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


def get_channel_videos(channel_id):
    res = youtube.channels().list(id="UC21TIh1Zzqo2RsoJRHGe_CA",
                                  part="contentDetails").execute()

    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part="snippet",
                                           pageToken=next_page_token,
                                           maxResults=50).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        if next_page_token is None:
            break
    return videos


api = "YOUR_YOUTUBE_API"
youtube = build("youtube","v3",
                developerKey=api)

videos = get_channel_videos("UC21TIh1Zzqo2RsoJRHGe_CA")
video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))
video_ids.reverse()
myRating = dict()
for i in video_ids:
    res = youtube.videos().list(id=i,
                                part='statistics').execute()
    stats = res['items']

    webpage = urllib.request.urlopen("http://www.youtube.com/watch?v="+i).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    title = ""
    for span in soup.findAll('span',
                             attrs={'class': 'watch-title'}):
        title = span.text.strip()
    myRating[title] = int(stats[0]['statistics']["viewCount"])/int(stats[0]['statistics']["likeCount"])
    myRating = {k: v for k, v in sorted(myRating.items(), key=lambda item: item[1])}
myRating = {k: v for k, v in sorted(myRating.items(), key=lambda item: item[1])}
count = 1
for i in myRating:
    print(str(count)+". "+str(myRating[i]))