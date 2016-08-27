from __future__ import absolute_import
from __future__ import division

import os
import logging
import csv

import tensorflow as tf
import numpy as np

from genres.csv_dataset import load_csv_without_header

from genres import config

logger = logging.getLogger(__name__)

out_dir = config['out_folder']
model_dir = '%s/%s' % (out_dir, 'model')
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

NET_CONFIG = config['network']
SPOTIFY_TRAINING = '%s/%s' % (out_dir, 'train.csv')
SPOTIFY_TEST = '%s/%s' % (out_dir, 'test.csv')

with open('%s/%s' % (out_dir, 'num_classes.txt')) as f:
    NUM_CLASSES = int(f.read())
with open('%s/%s' % (out_dir, 'num_features.txt')) as f:
    NUM_FEATURES = int(f.read())


def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def batch_norm_wrapper(inputs, is_training, decay=0.999):
    epsilon = NET_CONFIG['bn_epsilon']
    scale = tf.Variable(tf.ones([inputs.get_shape()[-1]]))
    beta = tf.Variable(tf.zeros([inputs.get_shape()[-1]]))
    pop_mean = tf.Variable(tf.zeros([inputs.get_shape()[-1]]), trainable=False)
    pop_var = tf.Variable(tf.ones([inputs.get_shape()[-1]]), trainable=False)

    if is_training is True:
        batch_mean, batch_var = tf.nn.moments(inputs,[0])
        train_mean = tf.assign(pop_mean,
                               pop_mean * decay + batch_mean * (1 - decay))
        train_var = tf.assign(pop_var,
                              pop_var * decay + batch_var * (1 - decay))
        with tf.control_dependencies([train_mean, train_var]):
            return tf.nn.batch_normalization(inputs, batch_mean, batch_var, beta, scale, epsilon)
    else:
        return tf.nn.batch_normalization(inputs, pop_mean, pop_var, beta, scale, epsilon)


def model(x, w_h, w_h2, w_o, p_keep_input, p_keep_hidden, is_training):
    x = tf.nn.dropout(x, p_keep_input)  # randomly lose some input to prevent overfitting
    z1 = tf.matmul(x, w_h)
    bn1 = batch_norm_wrapper(z1, is_training)  # normalize data
    h = tf.nn.relu(bn1)

    h = tf.nn.dropout(h, p_keep_hidden)
    z2 = tf.matmul(h, w_h2)
    bn2 = batch_norm_wrapper(z2, is_training)
    h2 = tf.nn.relu(bn2)

    h2 = tf.nn.dropout(h2, p_keep_hidden)

    return tf.matmul(h2, w_o)


def train():
    # initialize training sets
    training = load_csv_without_header(filename=SPOTIFY_TRAINING, n_classes=NUM_CLASSES,
                                       features_dtype=np.float64)
    test = load_csv_without_header(filename=SPOTIFY_TEST, n_classes=NUM_CLASSES,
                                   features_dtype=np.float64)
    tr_x, tr_y, te_x, te_y = training.data, training.target, test.data, test.target

    x = tf.placeholder(np.float32, [None, NUM_FEATURES])  # input
    y = tf.placeholder(np.float32, [None, NUM_CLASSES])  # output

    # initialize weights
    n_h = NET_CONFIG['nodes']
    w_h = init_weights([NUM_FEATURES, n_h])
    w_h2 = init_weights([n_h, n_h])
    w_o = init_weights([n_h, NUM_CLASSES])

    # establish model
    is_training = tf.placeholder(np.bool)
    p_keep_input = tf.placeholder(np.float32)
    p_keep_hidden = tf.placeholder(np.float32)
    py_x = model(x, w_h, w_h2, w_o, p_keep_input, p_keep_hidden, is_training)

    # determine loss function and training algorithm
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, y))
    train_op = tf.train.GradientDescentOptimizer(NET_CONFIG['learning_rate']).minimize(loss)
    predict_op = tf.argmax(py_x, 1)

    # initialize Saver so that data can be reused
    global_step = tf.Variable(0, name='global_step', trainable=False)
    saver = tf.train.Saver()
    with open('%s/%s' % (model_dir, 'training_data.csv'), 'ab') as training_csv:
        training_writer = csv.writer(training_csv)

        # Launch the graph in a session
        with tf.Session() as sess:
            tf.initialize_all_variables().run()

            # check if there's a re-initialization point
            checkpoint = tf.train.get_checkpoint_state(model_dir)
            if checkpoint and checkpoint.model_checkpoint_path:
                logger.info('Restarting from %s' % checkpoint.model_checkpoint_path)
                saver.restore(sess, checkpoint.model_checkpoint_path)  # restore all variables

            start = global_step.eval() + 1  # get last global_step

            batch_size = NET_CONFIG['batch_size']
            for i in range(start, NET_CONFIG['epochs']):
                for start, end in zip(range(0, len(tr_x), batch_size), range(batch_size, len(tr_x)+1, batch_size)):
                    # run training over each batch
                    sess.run(train_op, feed_dict={x: tr_x[start:end], y: tr_y[start:end],
                                                  p_keep_input: NET_CONFIG['p_keep_in'],
                                                  p_keep_hidden: NET_CONFIG['p_keep_hidden'],
                                                  is_training: True})

                global_step.assign(i).eval()  # set and update(eval) global_step with index, i
                saver.save(sess, '%s/%s' % (model_dir, "model.ckpt"), global_step=global_step)
                # record accuracy after each training session
                accuracy = np.mean(
                    np.argmax(te_y, axis=1) == sess.run(
                        predict_op, feed_dict={x: te_x, y: te_y, p_keep_input: 1.0,
                                               p_keep_hidden: 1.0, is_training: False}
                    )
                )
                training_writer.writerow([i, accuracy])
                logging.info('i=%s, accuracy=%s' % (i, accuracy))
