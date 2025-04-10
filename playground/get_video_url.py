from db_scripts.get_video_url import get_video_url

url = 'https://nhl.com/video/det-cbj-voronkov-scores-ppg-against-cam-talbot-6369506621112'

vurl = get_video_url(url)
print(vurl)