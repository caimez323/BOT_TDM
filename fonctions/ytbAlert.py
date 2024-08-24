import discord,os
from googleapiclient.discovery import build

# Remplacez par vos informations
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_CHANNEL_ID = 1270483670079111289  # ID du salon Discord
CHANNELS = {
    'EGO': 'UCxH16958KSxT4Z9yL_9JYtw',
    'TheGreatReview': 'UC2ruguOcwnVR2_4DtiGnmLg',
    "laiken" : "UC-VVYlox8h3JxxjyUe-6Zdw",
}

# Configuration de l'API YouTube
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
last_video_ids = {channel_name: None for channel_name in CHANNELS}


async def check_new_video(client):
    for channel_name, channel_id in CHANNELS.items():
        # Appel à l'API YouTube pour récupérer les vidéos les plus récentes
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=1,
            order='date'
        )
        response = request.execute()
        if response['items']:
            latest_video = response['items'][0]
            video_id = latest_video['id']['videoId']
            video_title = latest_video['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            if last_video_ids[channel_name] != video_id:
                last_video_ids[channel_name] = video_id
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                if channel:
                    await channel.send(f"Nouvelle vidéo de {channel_name} : **{video_title}**\n{video_url}")
                


