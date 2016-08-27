"""Base utilities for loading datasets.

Based on https://github.com/tensorflow/tensorflow/blob/r0.10/tensorflow/contrib/learn/python/learn/datasets/mnist.py
and https://github.com/tensorflow/tensorflow/blob/r0.10/tensorflow/contrib/learn/python/learn/datasets/base.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv

import numpy as np

from tensorflow.python.platform import gfile


class DataSet(object):
    def __init__(self, data, target):
        assert data.shape[0] == target.shape[0], \
            'data.shape: %s, target.shape: %s' % (data.shape, target.shape)
        self._data = data
        self._target = target
        self._index_in_epoch = 0
        self._epochs_completed = 0
        self._num_examples = data.shape[0]

    @property
    def data(self):
        return self._data

    @property
    def target(self):
        return self._target

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._data = self._data[perm]
            self._target = self._target[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._data[start:end], self._target[start:end]


Datasets = collections.namedtuple('Datasets', ['train', 'validation', 'test'])


def load_csv(filename, features_dtype, n_samples, n_features, n_classes, target_column=-1):
    """Load dataset from CSV file with a header row."""
    with gfile.Open(filename) as csv_file:
        data_file = csv.reader(csv_file)
        data = np.zeros((n_samples, n_features))
        target = np.zeros((n_samples,), dtype=np.int)
        for i, row in enumerate(data_file):
            t = np.zeros(n_classes)
            t[int(row.pop(target_column))] = 1
            target[i] = t
            data[i] = np.asarray(row, dtype=features_dtype)

    return DataSet(data=data, target=target)


def load_csv_without_header(filename, features_dtype, n_classes, target_column=-1):
    """Load dataset from CSV file without a header row."""
    with gfile.Open(filename) as csv_file:
        data_file = csv.reader(csv_file)
        data, target = [], []
        for row in data_file:
            t = np.zeros(n_classes)
            t[int(row.pop(target_column))] = 1
            target.append(t)
            data.append(np.asarray(row, dtype=features_dtype))

    target = np.array(target, dtype=np.int)
    data = np.array(data)
    return DataSet(data=np.array(data), target=np.array(target).astype(np.int))
