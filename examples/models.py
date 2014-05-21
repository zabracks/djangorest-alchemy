'''
Models
'''

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, ForeignKey
from sqlalchemy.types import INTEGER, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///sqlite.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

metadata = MetaData()


class Part(Base):
    __tablename__ = 'parts'

    car_id = Column(INTEGER, ForeignKey("cars.car_id"), primary_key=True)
    part_id = Column(INTEGER, primary_key=True)
    part_description = Column(String)
    part_num = Column(INTEGER)


class Car(Base):
    __tablename__ = 'cars'

    car_id = Column(INTEGER, primary_key=True)
    make = Column(String)
    model = Column(String)
    year = Column(String)
    parts = relationship(Part, uselist=True, primaryjoin=
                        (car_id == Part.car_id))


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
metadata.create_all(bind=engine)

car = Car(car_id='1', make='Toyota', model='Prius', year='2014')
part = Part(car_id='1', part_id='1', part_description='Engine', part_num='100')

session = Session()
session.add(car)
session.add(part)
session.commit()


class SessionMixin(object):
    def __init__(self, *args, **kwargs):
        self.session = Session()

        # This super is necessary
        # because in case of multiple inheritance
        # this calls the next __init__ in the MRO
        super(SessionMixin, self).__init__(*args, **kwargs)
