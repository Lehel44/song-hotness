import pandas as pd

# Read the tracks.csv to a pandas dataframe.
tracks = pd.read_csv('tracks.csv', index_col=0, header=[0, 1])

# The csv is multiindexed so we need to double-index the appropriate column to create a dataframe from them.
subset = tracks[[('artist', 'name'), ('track', 'title'), ('album', 'title'), ('album', 'date_created')]]

# Throw the rows which have any null value cells.
subset = subset[~subset.isnull().any(axis=1)]

# Select the artist and title columns as a new dataframe.
new_songs = subset[[('artist', 'name'), ('track', 'title')]]

# Drop the first index level.
new_songs.columns = new_songs.columns.droplevel()

# Create a new datadframe with flattening the remaining double indexeses.
song_full_title = pd.DataFrame(new_songs.to_records())

# Create a new column from artist name and track title as long_title.
song_full_title["long_title"] = song_full_title["name"] + " " + song_full_title["title"]


# Import the youtube data script.
import yt_view_count as yt

# Call the get_view_counts function with following parameter:
# dataframe, from row, to row, output file.
yt.get_view_counts(song_full_title, 40000, 45000, "yt_output_40000_44999.txt")