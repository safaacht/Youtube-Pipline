import os
from googleapiclient.discovery import build


API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")


youtube = build("youtube" , "v3" , developerKey = API_KEY)

channel_request = youtube.channels().list(
    part = "snippet , statistics , contentDetails" ,
    forHandle = CHANNEL_HANDLE
)

channel_response = channel_request.execute()

uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

all_videos = []
next_page_token = None

while True :
    video_request = youtube.playlistItems().list(
        part = "snippet , contentDetails",
        playlistId = uploads_playlist_id ,
        maxResults = 50 ,
        pageToken = next_page_token
    )

    video_response = video_request.execute()

    all_videos.extend(video_response["items"])
    next_page_token = video_response.get("nextPageToken")

    if not next_page_token :
        break


# print("Total videos extracted:", len(all_videos))
# print("First video ID:", all_videos[0]["contentDetails"]["videoId"])

video_ids = [
    video["contentDetails"]["videoId"]
    for video in all_videos
]

# print("Number of video IDs:", len(video_ids))

all_details = []

for i in range(0 , len(video_ids) , 50) :
    batch_ids = video_ids[i:i+50]

    details_request = youtube.videos().list(
        part = "snippet , contentDetails , statistics" ,
        id = ",".join(batch_ids)
    )


    details_response = details_request.execute()

    all_details.extend(details_response["items"])

print("Total video details:", (all_details))    