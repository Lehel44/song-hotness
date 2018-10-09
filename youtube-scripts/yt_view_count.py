import requests
import pandas as pd
from enum import Enum, auto

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#CLIENT_SECRETS_FILE = 'client_secret.json'
#DEVELOPER_KEY = 'AIzaSyBiZLPqvQv4RgVapUsLMUwdCB2hHLFn76g'
#DEVELOPER_KEY = 'AIzaSyD3mlN1JGOTe1kqjDVju_Suto-vkDUsRn0'
#DEVELOPER_KEY = 'AIzaSyAA3-XAFc_VCUcKkZMfzzItGbFC1SKaz_8'
DEVELOPER_KEY = 'AIzaSyDA_NoF5L4D9PnsbnrbBdpWtctDZaJJ9jI'
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

count = 0

class ErrorMessage(Enum):
  NOT_FOUND = auto()
  

def youtube_search(search_expr):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  global count
  print(count, "\n")
  count = count + 1

  search_response = youtube.search().list(
    q = search_expr,
    part = 'id,snippet',
    maxResults = 1,
	type = 'video'
  ).execute()
  
  response_items = search_response.get('items', [])
  result = ''
  try:
    result = response_items[0]['id']['videoId']
    if not result:
      return ErrorMessage.NOT_FOUND
  except KeyError:
    return ErrorMessage.NOT_FOUND
  except IndexError:
    return ErrorMessage.NOT_FOUND
  return response_items[0]['id']['videoId']
  
def get_view_counts(songs, from_, to_, file_name):
  output = open(file_name, 'w')
  
  # Slice dataframe
  songs = songs.iloc[from_ : to_]
  
  # Convert columns to arrays
  song_ids = songs["track_id"].values
  song_names = songs["long_title"].values
  
  for id, name in zip(song_ids, song_names):
    VIDEO_ID = youtube_search(name)
    if VIDEO_ID == ErrorMessage.NOT_FOUND:
      output.write('-1' + '\n')
      continue
	
    params = {
      'id': VIDEO_ID,
      'key': DEVELOPER_KEY
    }
    response = requests.get("https://www.googleapis.com/youtube/v3/videos?part=statistics", params = params)
    data = response.json()
	
    view_count = 0
    try:
      view_count = data["items"][0]["statistics"]["viewCount"]
      if not view_count:
        output.write('-1' + '\n')
      else:
        output.write(str(view_count) + '\n')
    except KeyError:
      output.write('-1' + '\n')
    except IndexError:
      output.write('-1' + '\n')
    except:
      output.write('-1' + '\n')

  output.close()