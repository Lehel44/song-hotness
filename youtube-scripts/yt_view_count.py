import requests
import pandas as pd
from enum import Enum, auto

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# API key created in Google Console API.
DEVELOPER_KEY = 'dummy'

# Properties to the Youtube Data API.
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# It which song the program at is. We ran it in 5000 song batches.
count = 0

# Enum class with auto value. The NOT_FOUND literal indicates
# that the view count of the songs wasn't find by the youtube_search
# function.
class ErrorMessage(Enum):
  NOT_FOUND = auto()
  
# It's looking for the given expression in YouTube database. Works like
# we type something on youtube.com and we get a result list but way quicker.
# search_expr: the expression to search on YouTube
# Returns the top result's video id.
def youtube_search(search_expr):

  # Build the YouTube API object with the set properties.
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  
  # Referring to the count declared outside, print and increase.
  global count
  print(count, "\n")
  count = count + 1

  # Get the search response where q is the search expression, and we need
  # the top result among videos.
  search_response = youtube.search().list(
    q = search_expr,
    part = 'id,snippet',
    maxResults = 1,
	type = 'video'
  ).execute()
  
  # We got a json as a result, need to get the view count. If any exception
  # occurs, we return with ErrorMessage.NOTFOUND, otherwise with video id.
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

# Get the view count from a video id.
# songs: dataframe
# from_, to_, indices to slice the dataframe
# file_name: output file path
# Returns the view count.
def get_view_counts(songs, from_, to_, file_name):
  output = open(file_name, 'w')
  
  # Slice dataframe
  songs = songs.iloc[from_ : to_]
  
  # Convert columns to arrays
  song_ids = songs["track_id"].values
  song_names = songs["long_title"].values
  
  # Iterate both arrays at once, so they're converted to tuples.
  # If video id is not found, return with -1, else do the search.
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
	
	# Trying to get the view count out of response json. If an exception occurs, write -1, otherwise
	# the view count.
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