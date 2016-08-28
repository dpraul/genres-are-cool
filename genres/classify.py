import os
import logging
import sys
import csv
import codecs

import numpy as np

from genres.features import spotify, get_features, SPOTIFY_TAGS, MULTIPLIERS
from genres.train import train
from genres import config

# change console to Unicode so that Python can print anything Spotify sends
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

logger = logging.getLogger(__name__)

out_dir = config['out_folder']
model_dir = '%s/%s' % (out_dir, 'model')
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

genres = {}
with open('%s/%s' % (out_dir, 'classes.csv')) as genre_csv:
    genre_reader = csv.reader(genre_csv)
    _ = genre_reader.next()  # skip header
    for row in genre_reader:
        genres[int(row[0])] = row[1]


def print_help():
    print 'run.py classify'
    print 'usage:'
    print '   python run.py classify [-t "spotify_id"] [-s "search terms"]'
    print 'example:'
    print '   python display_song.py -t "7GhIk7Il098yCjg4BQjzvb"'
    print '   python display_song.py -s "Killing in the Name Of"'
    print 'INPUTS'
    print '   [-t "spotify_id"] - classify the given Spotify ID'
    print '   [-s "search terms"] - interactive Spotify track search'


def start_classify():
    if len(sys.argv) < 4:
        print_help()
        return

    if sys.argv[2] == '-t':
        track_id = sys.argv[3]
        classify_track(track_id)
    elif sys.argv[2] == '-s':
        query = sys.argv[3]
        search_spotify(query)
    else:
        print_help()


def search_spotify(query):
    r = spotify.search(query, type='track', limit=10)
    if ('tracks' not in r and len(r['tracks']) == 0
            or 'items' not in r['tracks'] or len(r['tracks']['items']) == 0):
        logger.info('No tracks found')
        return
    items = r['tracks']['items']

    # Assemble choices
    choices = []
    for item in items:
        if 'type' not in item or item['type'] != 'track':
            continue
        choices.append({'id': item['id'], 'title': item['name'], 'artist': ''})
        if 'artists' in item and len(item['artists']) > 0:
            artist = item['artists'][0]
            if 'name' in artist:
                choices[-1]['artist'] = artist['name']

    # Show choices
    for i, choice in enumerate(choices):
        print('[%s] %s - %s' % (i, choice['title'], choice['artist']))
    try:
        user_choice = input('\nChoose a track (-1 for quit): ')
    except SyntaxError:
        return

    if user_choice < 0 or user_choice > len(choices):
        return

    classify_track(choices[user_choice]['id'])


def classify_track(track_id):
    features = get_features(track_id)[0]
    if features is None or 'id' not in features:
        logger.error('The id %s was not found in the Spotify feature database' % track_id)

    x = np.zeros((1, len(SPOTIFY_TAGS)))
    for i, key in enumerate(SPOTIFY_TAGS):
        if key not in SPOTIFY_TAGS:
            logger.warn('%s was not found in the Spotify feature tags - '
                        'classification more likely to be incorrect' % key)
            x[1, i] = features[key] * MULTIPLIERS[i]

    genre_index = train(x)
    genre = genres[genre_index]
    print('\n%s is predicted to be %s' % (track_id, genre))
