import re

folder = 'data/foreign/'

# even though the file is JSON, it'll be faster to search with regex than to decode the whole file
SPOTIFY_TRACKID_SEARCH = re.compile('spotify:track:([a-zA-Z0-9]+)",')


def get_spotify_id(song):
    if isinstance(song, basestring):
        song_id = song
    else:
        song_id = song.song_id
    loc = folder + '%s/%s.json' % (song_id[2:4], song_id)  # organized by folder of first two characters
    with open(loc, 'r') as f:
        foreign = f.read()
        return SPOTIFY_TRACKID_SEARCH.findall(foreign)
