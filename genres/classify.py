import sys
from genres.features import spotify


def classify():
    pass


def print_help():
    print 'display_song.py'
    print 'usage:'
    print '   python display_song.py <command>'
    print 'example:'
    print '   python display_song.py graph'
    print 'INPUTS'
    print '   <command> - build, graph'


def start_classify():
    if len(sys.argv) < 3:
        print_help()
        return
    pass