from __future__ import absolute_import
from __future__ import division

import logging
import sys

from genres import config

if config['logging'] == 'console':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(message)s',
        level=logging.DEBUG
    )
elif config['logging'] == 'file':
    logging.basicConfig(
        filename='output.log',
        format='%(asctime)s - %(name)s - %(message)s',
        level=logging.DEBUG
    )


def print_help():
    print 'run.py'
    print 'usage:'
    print '   python run.py <command>'
    print 'example:'
    print '   python run.py graph'
    print 'INPUTS'
    print '   <command> - build, graph, train, classify'


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    if command == 'build':
        from genres.fill_database import fill_from_list
        fill_from_list()
    elif command == 'graph':
        from genres.graph import make_graphs
        make_graphs()
    elif command == 'train':
        from genres.train import train
        train()
    elif command == 'classify':
        from genres.classify import start_classify
        start_classify()
    else:
        print_help()

if __name__ == '__main__':
    main()
