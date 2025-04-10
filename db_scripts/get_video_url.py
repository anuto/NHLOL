import requests
from bs4 import BeautifulSoup
import json

ACCOUNT = 'D3UCGynRWU_default'

def get_video_url(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with the specific data-plugin attribute
        div_element = soup.find('div', {'data-plugin': 'bc-video-player-events'})
        
        if div_element:

            # Get the data-options attribute
            data_options_raw = div_element.get('data-options')
            
            if data_options_raw:
                # Convert the JSON string to a Python dictionary
                data_options = json.loads(data_options_raw)

                if not data_options:
                    return
                        
                brightcove_account = data_options['brightcoveAccount']
                video_id = data_options['brightcoveVideoId']

                url = 'https://players.brightcove.net/' + brightcove_account + '/' + ACCOUNT + '/index.html?videoId=' + video_id
                return url
            else:
                print(url)
                print("data-options attribute not found.")

        else:
            print(url)
            print("Div with data-plugin='bc-video-player-events' not found.")
    else:
        print(url)
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return