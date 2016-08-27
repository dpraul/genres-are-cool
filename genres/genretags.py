import os
import json

datasets = {
    'yajie': {
        'folder': 'data/GenreTags',
        'txt': 'GenreTags.txt',
        'json': 'GenreTags.json',
        'skip': 23
    },
    'tagtraum_cd2': {
        'folder': 'data/tagtraum',
        'txt': 'msd_tagtraum_cd2.cls',
        'json': 'msd_tagtraum_cd2.json',
        'skip': 7
    },
    'tagtraum_cd2c': {
        'folder': 'data/tagtraum',
        'txt': 'msd_tagtraum_cd2c.cls',
        'json': 'msd_tagtraum_cd2c.json',
        'skip': 7
    }
}


def _get_genres_from_txt(dataset):
    genres = {}

    with open('%s/%s' % (dataset['folder'], dataset['txt']), 'r') as f:
        for i, line in enumerate(f):
            if i < dataset['skip']:
                continue
            data = line.split('\t', 2)
            track_id = data[0]
            genre = data[1].replace('\n', '')
            genres[track_id] = genre

    with open('%s/%s' % (dataset['folder'], dataset['json']), 'w') as f:
        json.dump(genres, f)

    return genres


def _get_genres_from_json(dataset):
    with open('%s/%s' % (dataset['folder'], dataset['json']), 'r') as f:
        return json.load(f)


def get_genre_map(dataset_name):
    dataset = datasets[dataset_name]

    if os.path.isfile('%s/%s' % (dataset['folder'], dataset['json'])):
        return _get_genres_from_json(dataset)
    return _get_genres_from_txt(dataset)
