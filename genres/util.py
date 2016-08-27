def chunks_iterable(iterable, size):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(iterable), size):
        yield iterable[i:i + size]


def chunks_range(stop, size):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, stop, size):
        yield xrange(i, i + size)
