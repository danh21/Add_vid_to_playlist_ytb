import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import urllib.parse

SCOPES = ["https://www.googleapis.com/auth/youtube"]

CACHE_FILE = "added_videos.json"  # cache added videos to avoid duplicates

def get_youtube_service():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

def get_uploads_playlist_id(youtube, url):
    channel_id = None

    if "/channel/" in url:
        channel_id = url.split("/channel/")[-1]
    else:
        username = url.split("/")[-1]
        username = urllib.parse.unquote(username)  # decode %E1%BA...
        request = youtube.search().list(
            part="snippet",
            q=username,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        items = response.get("items")
        if not items:
            raise ValueError(f"Not found channel with username: {username}")      
        channel_id = items[0]["snippet"]["channelId"]

    # Now get uploads playlist from channelId
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()
    items = response.get("items")
    if not items:
        raise ValueError("Not found channel to get uploads playlist")
    uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return uploads_playlist_id

def get_all_video_ids_from_playlist(youtube, playlist_id):
    video_ids = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response.get("items", []):
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_cache(video_ids):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(video_ids), f)

if __name__ == "__main__":
    channel_url = input("Enter channel URL: ").strip()
    target_playlist_id = input("Enter playlist ID: ").strip()
    max_per_run = 200  # maximum number of videos to add per run

    youtube = get_youtube_service()
    uploads_playlist_id = get_uploads_playlist_id(youtube, channel_url)
    print("Getting list of videos in channel...")
    all_video_ids = get_all_video_ids_from_playlist(youtube, uploads_playlist_id)
    print(f"Sum of videos in channel: {len(all_video_ids)}")

    # load videos already added from cache
    added_videos = load_cache()
    print(f"Previously added: {len(added_videos)}")
    # select new videos to add
    to_add = [v for v in all_video_ids if v not in added_videos][:max_per_run]
    print(f"Number of videos to add this time: {len(to_add)}")

    for vid in to_add:
        try:
            add_video_to_playlist(youtube, target_playlist_id, vid)
            added_videos.add(vid)
            print(f"Added: {vid}")
        except Exception as e:
            print(f"Failed to add {vid}: {e}")

    # update cache
    save_cache(added_videos)
    print("DONE! 🎉")
