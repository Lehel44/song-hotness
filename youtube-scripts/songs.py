
# coding: utf-8

# In[1]:


import pandas as pd

tracks = pd.read_csv('tracks.csv', index_col=0, header=[0, 1])
pd.set_option("max_columns",None)
tracks


# In[2]:


artist = tracks['artist', 'name']


# In[3]:


artist.head()


# In[4]:


song = tracks['track', 'title']
song.head()


# In[5]:



artist_song = pd.concat([artist, song], axis = 1)
artist_song.head()


# In[6]:


subset = tracks[[('artist', 'name'), ('track', 'title'), ('album', 'title'), ('album', 'date_released'), ('album', 'date_created')]]
subset


# In[7]:


ndate = subset[[('album', 'date_released'), ('album', 'date_created')]].min(axis=1)


# In[8]:


subset[[('album', 'date_released'), ('album', 'date_created')]]


# In[9]:


subset2 = tracks[[('artist', 'name'), ('track', 'title'), ('album', 'title'), ('album', 'date_released')]]
subset3 = tracks[[('artist', 'name'), ('track', 'title'), ('album', 'title'), ('album', 'date_created')]]
subset2 = subset2[~subset2.isnull().any(axis=1)]
subset3 = subset3[~subset3.isnull().any(axis=1)]


# In[10]:


subset2.shape


# In[11]:


subset3.shape


# In[12]:


subset4 = subset[~subset[[('album', 'date_released'), ('album', 'date_created')]].isnull().any(axis=1)]


# In[13]:


subset4.shape


# In[35]:


new_songs = subset3[[('artist', 'name'), ('track', 'title')]]
new_songs.columns = new_songs.columns.droplevel()

new_songs


# In[38]:


#song_full_title = pd.DataFrame(columns = ["full_title"])
#song_full_title["full_title"] = new_songs["artist", "name"] + " " + new_songs["track", "title"]
song_full_title = pd.DataFrame(new_songs.to_records())
song_full_title["long_title"] = song_full_title["name"] + " " + song_full_title["title"]



import yt_view_count as yt

yt.get_view_counts(song_full_title, 50000, 55000, "yt_output_50000_54999.txt")

