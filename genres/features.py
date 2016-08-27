from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify

from genres import config

SPOTIFY_TAGS = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness',
                'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']

client_credentials_manager = SpotifyClientCredentials(client_id=config['spotify']['id'],
                                                      client_secret=config['spotify']['secret'])
spotify = Spotify(client_credentials_manager=client_credentials_manager)


def get_features(track_ids):
    """ Get audio features for the given track ID's. Maximum of 100 id's

    See https://developer.spotify.com/web-api/get-several-audio-features/ for more info.

    :param collections.List[str] track_ids:
    :return:
    """
    if isinstance(track_ids, basestring):
        track_ids = [track_ids, ]
    if len(track_ids) > 100:
        raise IndexError('Too many tracks specified.')

    return spotify.audio_features(track_ids)
