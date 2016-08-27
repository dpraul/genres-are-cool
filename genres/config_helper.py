import yaml
import os.path


def read_config(filename, env):
    if not os.path.isfile(filename):
        raise IOError('The file %s is not found' % filename)

    with open(filename, 'r') as f:
        doc = yaml.load(f)

    if env not in doc:
        raise ValueError("Specified environment doesn't exist in config file")

    return doc[env]
