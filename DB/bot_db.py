from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker, relationship

# def create_db():
engine = create_engine('postgresql+psycopg2://postgres:0206@localhost/BotTryDB')
meta = MetaData(engine)

heroes = Table('heroes', meta, autoload=True)
admins = Table('admins', meta, autoload=True)

class Hero():
    def __init__(self, hero_id, hero_name, hero_power_level, hero_photo_id):
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.hero_power_level = hero_power_level
        self.hero_photo_id = hero_photo_id

    def __repr__(self):
        return "<Hero(%s, %s, %s, %s)>" % (self.hero_id, self.hero_name, self.hero_power_level, self.hero_photo_id)

class Admin():
    def __init__(self, admin_name, admin_id):
        self.admin_name = admin_name
        self.admin_id = admin_id

    def __repr__(self):
        return '<Admins(%s, %s)>' % (self.admin_id, self.admin_name)

mapper(Hero, heroes)
mapper(Admin, admins)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.commit()
