import os
import json

filename_txt = 'data/MSD/unique_tracks.txt'
filename_json = 'data/MSD/unique_tracks.json'


def _get_tracks_txt():
    tracks = {}

    with open(filename_txt, 'r') as f:
        for i, line in enumerate(f):
            track_id, song_id, _, _ = line.split('<SEP>')
            tracks[track_id] = song_id

    with open(filename_json, 'w') as f:
        json.dump(tracks, f)

    return tracks


def _get_tracks_json():
    with open(filename_json, 'r') as f:
        return json.load(f)


def get_all_tracks():
    if os.path.isfile(filename_json):
        return _get_tracks_json()
    return _get_tracks_txt()
