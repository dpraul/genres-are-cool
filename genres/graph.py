import os
import csv

import numpy as np
import matplotlib.pyplot as plt


from genres import Song, Session
from genres.features import SPOTIFY_TAGS, SKIP_TAGS, MULTIPLIERS

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

    all_tags = [tag for tag in SPOTIFY_TAGS if tag not in SKIP_TAGS]
    mul = [m for i, m in enumerate(MULTIPLIERS) if SPOTIFY_TAGS[i] not in SKIP_TAGS]

    datamap = {tag: {genre: np.empty(q.count()) for genre in all_genres} for tag in all_tags}

    # get ready to save CSV files
    training_csv = open('%s/%s' % (out_folder, 'train.csv'), 'wb')
    training_writer = csv.writer(training_csv)

    test_csv = open('%s/%s' % (out_folder, 'test.csv'), 'wb')
    test_writer = csv.writer(test_csv)

    all_csv = open('%s/%s' % (out_folder, 'all.csv'), 'wb')
    all_writer = csv.writer(all_csv)

    header = all_tags + ['genre', ]  # theoretical header for each CSV

    # this row will be used to write each row
    empty_row = [0 for _ in header]

    for i, row in enumerate(q):
        for j, tag in enumerate(all_tags):
            attr = getattr(row, tag) * mul[j]
            empty_row[j] = attr
            datamap[tag][row.genre][genre_data_count[row.genre]] = attr

        empty_row[-1] = genre_index[row.genre]
        genre_data_count[row.genre] += 1

        all_writer.writerow(empty_row)
        if i % 10 == 0:  # take about a 10th of the data and use it as testing data
            test_writer.writerow(empty_row)
        else:
            training_writer.writerow(empty_row)

    # package data for TensorFlow
    all_csv.close()
    training_csv.close()
    test_csv.close()

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

    with open('%s/%s' % (out_folder, 'classes.csv'), 'wb') as classes_csv:
        classes_writer = csv.writer(classes_csv)
        classes_writer.writerow(['class', 'genre', 'count'])
        for genre in all_genres:
            classes_writer.writerow([genre_index[genre], genre, genre_data_count[genre]])

    with open('%s/%s' % (out_folder, 'num_classes.txt'), 'w') as f:
        f.write('%s' % len(all_genres))

    with open('%s/%s' % (out_folder, 'num_features.txt'), 'w') as f:
        f.write('%s' % len(all_tags))

    plt.show()
