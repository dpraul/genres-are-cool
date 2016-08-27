import os
import csv

import numpy as np
import matplotlib.pyplot as plt


from genres import Song, Session
from genres.features import SPOTIFY_TAGS

from genres import config

graph_folder = 'graphs/%s' % config['genre_dataset']
out_folder = config['out_folder']

if not os.path.exists(graph_folder):
    os.makedirs(graph_folder)  # directory to save graphs
if not os.path.exists(out_folder):
    os.makedirs(out_folder)  # directory to save graphs
session = Session()


def make_graphs():
    genres_query = session.query(Song.genre.distinct().label('genre'))
    all_genres = [row.genre for row in genres_query.all()]
    genre_index = {genre: i for i, genre in enumerate(all_genres)}
    genre_data_count = {genre: 0 for genre in all_genres}

    q = session.query(Song)

    datamap = {tag: {genre: np.empty(q.count()) for genre in all_genres} for tag in SPOTIFY_TAGS}

    csvfile = open('%s/%s' % (out_folder, 'data.csv'), 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(SPOTIFY_TAGS + ['genre', ])

    empty_row = [0 for _ in SPOTIFY_TAGS] + [0, ]

    for i, row in enumerate(q):
        for j, tag in enumerate(SPOTIFY_TAGS):
            attr = getattr(row, tag)
            empty_row[j] = attr
            datamap[tag][row.genre][genre_data_count[row.genre]] = attr

        empty_row[-1] = genre_index[row.genre]
        writer.writerow(empty_row)
        genre_data_count[row.genre] += 1

    csvfile.close()  # save all the data into a CSV file for TensorFlow

    for tag, genremap in datamap.iteritems():
        # resize datamap arrays to get rid of empty cells
        for genre, data in genremap.iteritems():
            data.resize([1, genre_data_count[genre]], refcheck=False)
            genremap[genre] = data

        fig = plt.figure(figsize=(15, 6))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(genremap.values(), labels=genremap.keys(), showmeans=True, showfliers=False)
        ax.set_title(tag)
        fig.savefig('%s/%s.png' % (graph_folder, tag), bbox_inches='tight')

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    pie = ax.pie(genre_data_count.values(), labels=genre_data_count.keys())
    ax.set_title('Genre Distribution')
    fig.savefig('%s/%s.png' % (graph_folder, 'genres'), bbox_inches='tight')

    with open('%s/%s' % (out_folder, 'classes.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['class', 'genre', 'count'])
        for genre in all_genres:
            writer.writerow([genre_index[genre], genre, genre_data_count[genre]])

    with open('%s/%s' % (out_folder, 'num_classes.txt'), 'w') as f:
        f.write('%s' % len(all_genres))

    plt.show()
