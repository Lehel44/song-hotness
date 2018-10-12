


# Deep learning homework: Song hotness  - Data exploration

## The exercise

We decided to create a neural network that decides whether a song will be popular or not. We measured the popularity of songs with YouTube view counts and we're going to try different subsets of song attributes to teach the neural network in order the get better predictions. We will also try how the prediction goes if we teach with songs of all time or songs after 2010.

## Data sources

We used the Free Music Archive github repository (https://github.com/mdeff/fma) to get songs with various attributes and used YouTube to decide how popular a song is. The dataset is a dump of the [Free Music Archive (FMA)](https://freemusicarchive.org/), an interactive library of high-quality, legal audio downloads.


All metadata and features for all tracks are distributed in  **[fma_metadata.zip](https://os.unil.cloud.switch.ch/fma/fma_metadata.zip)**  (342 MiB). The below tables can be used with  [pandas](http://pandas.pydata.org/)  or any other data analysis tool. See the  [paper](https://arxiv.org/abs/1612.01840)  or the  [usage](https://nbviewer.jupyter.org/github/mdeff/fma/blob/outputs/usage.ipynb)  notebook for a description.

-   `tracks.csv`: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.
-   `genres.csv`: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
-   `features.csv`: common features extracted with  [librosa](https://librosa.github.io/librosa/).
-   `echonest.csv`: audio features provided by  [Echonest](http://the.echonest.com/)  (now  [Spotify](https://www.spotify.com/)) for a subset of 13,129 tracks.

## YouTube data mining
We assumed that if a song was popular at any time then it has significantly higher view count than other videos have. Our first try was to use the YouTube Data API that provides access to the properties of youtube channels, videos etc. for developers. It's basically a hidden REST API communicating with YouTube in json format. The *yt_view_count.py* script is out implementation using this API to search for a video and retrieve it's view count. Later turned out Google limits the usage of the API based on quota per day and we didn't have enough time for that.

 We tried another approach; avoid using the YouTube API, just scrape the information from html code. The *view_count_scraper.py* is our implementation. The first problem was that the program was running with one thread and it was slow. It would have taken two weeks to get its job done. When we modified the code to use multithreading, YouTube detected that we are scraping their site and we got a ban. Next thing we tried was to use rotating proxy to avoid the IP ban. We successfully implemented this part, but it took so much time that it'd take months.

We returned to the first approach and successfully bypassed the quota limitation by creating new projects with new API key, or creating new google accounts. We tried to get 100.000 song's view count and ran the script in 5000 song batches not to overrun the quota. It took about one hour for each to get the view counts.

## Data preparation

We used *pandas* python package to work with *csv* data and dataframes. The first problem was the multiindexed csv data, that was really hard to work with in pandas. We fixed the problem in excel and deleted manually the higher indices, so a mono-indexed csv remained.

We cleaned the dataframe, deleted the unrelevant columns which had *NaN* or interpolated values, or it just had nothing to do with song popularity (for instance Wikipedia url link). Then we transformed the language and location attributes to categorical attributes. Kept the first 9, and named *others* the remaining ones.

We joined the view count column retrieved by the *yt_view_count script* and normalized the values.

## References

 FMA: A Dataset For Music Analysis
[Michaël Defferrard](https://arxiv.org/search/cs?searchtype=author&query=Defferrard%2C+M),  [Kirell Benzi](https://arxiv.org/search/cs?searchtype=author&query=Benzi%2C+K),  [Pierre Vandergheynst](https://arxiv.org/search/cs?searchtype=author&query=Vandergheynst%2C+P),  [Xavier Bresson](https://arxiv.org/search/cs?searchtype=author&query=Bresson%2C+X)