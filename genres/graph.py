import os

import numpy as np
import matplotlib.pyplot as plt


from genres import Song, Session
from genres.features import SPOTIFY_TAGS

from genres import config

folder = 'graphs/%s' % config['genre_dataset']
os.makedirs(folder)  # directory to save graphs
session = Session()


def make_graphs():
    genres_query = session.query(Song.genre.distinct().label('genre'))
    all_genres = [row.genre for row in genres_query.all()]
    genre_data_count = {genre: 0 for genre in all_genres}

    q = session.query(Song)

    all_data = np.empty([q.count(), len(SPOTIFY_TAGS)])
    genres = ['' for _ in xrange(q.count())]
    datamap = {tag: {genre: np.empty(q.count()) for genre in all_genres} for tag in SPOTIFY_TAGS}

    for i, row in enumerate(q):
        for j, tag in enumerate(SPOTIFY_TAGS):
            attr = getattr(row, tag)
            all_data[i, j] = attr
            datamap[tag][row.genre][genre_data_count[row.genre]] = attr

        genres[i] = row.genre
        genre_data_count[row.genre] += 1

    for tag, genremap in datamap.iteritems():
        # resize datamap arrays to get rid of empty cells
        for genre, data in genremap.iteritems():
            data.resize([1, genre_data_count[genre]], refcheck=False)
            genremap[genre] = data

        fig = plt.figure(figsize=(15, 6))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(genremap.values(), labels=genremap.keys(), showmeans=True, showfliers=False)
        ax.set_title(tag)
        fig.savefig('%s/%s.png' % (folder, tag), bbox_inches='tight')

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    pie = ax.pie(genre_data_count.values(), labels=genre_data_count.keys())
    ax.set_title('Genre Distribution')
    fig.savefig('%s/%s.png' % (folder, 'genres'), bbox_inches='tight')
    print genre_data_count

    plt.show()
