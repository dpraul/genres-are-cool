# Genres are cool!

The original goal was to use the [MillionSongDataset (MSD)](http://labrosa.ee.columbia.edu/millionsong/)
and machine learning to predict the genre of any given song. But, the MSD contains useful audio features
calculated using proprietary algorithms by EchoNest. Since EchoNest is now owned by Spotify,
those features can only be gathered for songs on Spotify using the [Spotify Web API](https://developer.spotify.com/web-api/get-audio-features/).

To accommodate, the goal of the project is to create a machine learning algorithm that can predict song
genre using those Spotify audio features. To do this, a new database of features must be generated using
the MSD and Spotify Web API.

## 1. Requirements

All requirements can be installed by running `pip install -r requirements.txt` inside a virtualenv. The packages used are:

 - SQLAlchemy
 - matplotlib
 - numpy
 - pytables
 - TensorFlow
 - spotipy
 
Spotify OAuth credentials are needed to get song analysis information. Copy `config_sample.yml` to a new file 
`config.yml` and replace the Spotify client_id and client_secret with your OAuth credentials.
 
## 2. Data

The whole MSD is not actually needed, as the relevant features will be grabbed using the Spotify Web API.
In place of the whole MSD, we will use the [database linking EchoNest track id to song id](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_tracks.txt).
Place this file in `data/MSD/unique_tracks.txt`.

To associate Spotify track id with each EchoNest song id, we will use the [AcousticBrainz mapping archive](http://labs.acousticbrainz.org/million-song-dataset-echonest-archive).
Extract the .tar.bz2 file to `data/foreign/`
(the directory structure should look like `data/foreign/AA/`, `data/foreign/AB/`, `data/foreign/AC/`, etc.).

Lastly, a genre mapping for the MSD is needed. There are several available:
  
 - [last.fm dataset](http://labrosa.ee.columbia.edu/millionsong/lastfm)
 - [tagtraum genre annotations](http://www.tagtraum.com/msd_genre_datasets.html)
 - [yajie hu's genre tagging](http://web.cs.miami.edu/home/yajiehu/resource/genre/index.html)

The project has been tested to work with either the tagtraum or yajie dataset. The charts and analysis done
are only done with the tagtraum_cd2c dataset.

If using the tagtraum dataset, pick either [msd_tagtraum_cd2](http://www.tagtraum.com/genres/msd_tagtraum_cd2.cls.zip)
or [msd_tagtraum_cs2c](http://www.tagtraum.com/genres/msd_tagtraum_cd2c.cls.zip) and unzip it to 
`data/tagtraum/FILE.cls`. 

If using yajie hu's mapping, extract it to `data/GenreTags/GenreTags.txt`.

Change the `genre_dataset` key in `config.yml` to either `tagtraum_cd2`, `tagtraum_cd2c`, or `yaji`, matching
the choice you made.

## 3. Building the database

Firstly, the new Spotify database has to be built. To do this, run `python run.py build`. This might take a while as it can only
get information for 100 songs at a time from Spotify and sleeps for 15 seconds every 100 queries to avoid rate limiting.

After it is finished, the file `data/db/all.db` should be created, and if explored with a SQLite
explorer will show about 27,000 entries using tagtraum's cd2c.


## 4. Graphs


## References

https://github.com/jazdev/genreXpose

https://github.com/tbertinmahieux/MSongsDB
