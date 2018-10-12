from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool
from fake_useragent import UserAgent
import requests
import re
import random

SEARCH_BASE = "https://www.youtube.com/results?search_query="
YT_BASE = "https://www.youtube.com/"
counter = 0

# The script is based on https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/
# article.

# Scrapes the latest proxies from sslproxies.org.
def get_latest_proxies():
  ua = UserAgent()
  proxies = []
  
  # Retrieve latest proxies
  headers = {'User-Agent' : ua.random}
  proxies_req = requests.get('https://www.sslproxies.org/', headers = headers)
  proxies_doc = proxies_req.content
  
  # Parse it to BeautifulSoup object.
  soup = bs(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append(
      "https://" + row.find_all('td')[0].string + ":" + row.find_all('td')[1].string
    )
  return proxies

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy(proxies):
  return random.randint(0, len(proxies) - 1)

def request_proxy_url(url):
  # Get latest proxies
  proxies = get_latest_proxies()

  # Choose an initial random proxy
  proxy_index = random_proxy(proxies)
  proxy = proxies[proxy_index]
  
  # While proxy is not succeed, try to get another one and make
  # the parameter request with the headers.
  proxy_succeed = False
  
  while not proxy_succeed:
    proxy_dict = { 
      "http"  : proxy, 
      "https" : proxy
    }
    headers = {
      'User-Agent' : ua.random
    }
    response = None
    try:
      response = requests.get(url, headers = headers, proxies = proxy_dict)
      proxy_succeed = True
    except:
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

  return response

# This function uses the request_proxy_url with the appropriate urls
# to scrape view numbers from YouTube.
def get_single_view_count(search_expr):

  # Counter to see where the program is at.
  global counter
  counter = counter + 1
  print(counter, "\n")
  
  # Try to get view count. If an exception occurs return -1,
  # otherwise the view count.
  try:
    search_page = request_proxy_url(SEARCH_BASE + search_expr)
    #search_page = requests.get(SEARCH_BASE + search_expr, headers = headers, proxies = proxy_dict)
    soup = bs(search_page.content, 'html.parser')
    
    first_video_id = soup.find(class_=" yt-uix-sessionlink spf-link ")["href"]
    video_page = request_proxy_url(YT_BASE + first_video_id)

    soup = bs(video_page.content, 'html.parser')

    view_count_tag = soup.find(class_="stat view-count").string
    view_count_array = re.findall(r'\d+', view_count_tag)
    view_count = "".join(view_count_array)
  except:
    return "-1"

  return view_count

# Slices the dataframe, creates a thread pool to speed up things.
# It maps the song names to the get_single_view_count function,
# because map has a threaded implementation. It works well with
# multiprocessing.dummy package.
def get_view_count(songs, from_, to_):

  songs = songs.iloc[from_ : to_ + 1]
  
  song_ids = songs["track_id"].values
  song_names = songs["long_title"].values

  pool = ThreadPool(10)
  view_counts = pool.map(get_single_view_count, song_names)
  
  pool.close() 
  pool.join()

  output = open('yt_output_1_5000.txt', 'w')
  for (id, view_count) in zip(song_ids, view_counts):
    output.write(str(id) + "," + view_count + "\n")
  output.close()



