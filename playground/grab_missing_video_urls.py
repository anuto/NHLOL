from db_scripts.get_video_url import get_video_url

url = 'https://www.nhl.com/gamecenter/bos-vs-cgy/2024/11/07/2024020208/summary'

video_url = get_video_url(url)
print(video_url)