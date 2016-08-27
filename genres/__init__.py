from config_helper import read_config
config = read_config('config/config.yml', 'default')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(config['database'], echo=config['debug'])
Base = declarative_base()

from models import *  # load database models

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
