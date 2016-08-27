import logging
import sys

from genres.fill_database import fill_from_list
from genres.graph import make_graphs

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.DEBUG
)


def print_help():
    print 'display_song.py'
    print 'usage:'
    print '   python display_song.py <command>'
    print 'example:'
    print '   python display_song.py graph'
    print 'INPUTS'
    print '   <command> - build, graph'


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    if command == 'build':
        fill_from_list()
    elif command == 'graph':
        make_graphs()


if __name__ == '__main__':
    main()
