import logging
import time

from genres.features import get_features, SPOTIFY_TAGS
from genres.msd import SongEntries
from genres.msdlist import get_all_tracks
from genres.foreign import get_spotify_id
from genres.genretags import get_genre_map
from genres.util import chunks_range

from genres import Session, Song

from genres import config

logger = logging.getLogger(__name__)
session = Session()
genres = get_genre_map(config['genre_dataset'])

SLEEP_TIME = 15


def fill_from_aggregate():
    """  Fills the SQLAlchemy database given an aggregate h5 file.

    Aggregate file can be created from
    https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/create_aggregate_file.py
    """
    filename = 'data/MSD/aggregate.h5'

    msd = SongEntries(filename)
    for chunk in chunks_range(msd.num_songs, 100):  # chunks of 100 so we can perform batches of Spotify grabs
        batch = {}  # spotifyId: Song

        for i in chunk:
            msd.songidx = i  # loop over every song contained in the aggregate file

            if msd.track_id not in genres:
                logger.warning('%s has no genre in %s' % (msd.track_id, config['genre_dataset']))
                continue
            genre = genres[msd.track_id]

            spotify_ids = get_spotify_id(msd)
            if len(spotify_ids) == 0:
                logger.warning('%s has no Spotify id' % msd.track_id)
                continue
            spotify_id = spotify_ids[0]  # we'll assume the first Spotify ID is fine

            song = Song(msd.track_id)
            song.song_id = msd.song_id
            song.spotify_id = spotify_id
            song.genre = genre

            batch[spotify_id] = song

        features_batch = get_features(batch.keys())
        for features in features_batch:
            song = batch[features['id']]
            for key in SPOTIFY_TAGS:
                if key not in features:
                    logger.warning('%s not found on Spotify for %s' % (key, song.track_id))
                    continue
                setattr(song, key, features[key])

            session.add(song)
            logger.info('Added %s to session.' % song.track_id)

        session.commit()
        logger.info('Committed %s songs to database, ending at batchid=%s.' % (len(batch), msd.songidx))


def fill_from_list():
    tracks = get_all_tracks()

    batch = {}  # spotifyId: Song
    i = -1
    for track_id, song_id in tracks.iteritems():
        i += 1
        if i < 15199:
            continue
        if track_id not in genres:
            logger.warning('%s has no genre in %s' % (track_id, config['genre_dataset']))
            continue
        genre = genres[track_id]

        spotify_ids = get_spotify_id(song_id)
        if len(spotify_ids) == 0:
            logger.warning('%s has no Spotify id' % track_id)
            continue
        spotify_id = spotify_ids[0]  # we'll assume the first Spotify ID is fine

        song = Song(track_id)
        song.song_id = song_id
        song.spotify_id = spotify_id
        song.genre = genre

        batch[spotify_id] = song

        if len(batch) == 100 or i == len(tracks) - 1:  # send a batch if we hit 100 songs or if it's the last batch
            features_batch = get_features(batch.keys())
            for features in features_batch:
                if features is None or 'id' not in features:
                    logger.warning("One of the Spotify id's turned up a bad response. Hard to tell which.")
                    continue
                song = batch[features['id']]
                for key in SPOTIFY_TAGS:
                    if key not in features:
                        logger.warning('%s not found on Spotify for %s' % (key, song.track_id))
                        continue
                    setattr(song, key, features[key])

                session.merge(song)
                logger.info('Added %s to session.' % song.track_id)

            session.commit()
            logger.info('Committed %s songs to database, ending at i=%s, track_id=%s' % (len(batch), i, track_id))
            batch = {}

        if i % 10000 == 0:
            logger.info('Sleeping for %s seconds so hopefully Spotify has mercy on us.' % SLEEP_TIME)
            time.sleep(SLEEP_TIME)
