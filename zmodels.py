#!/usr/bin/env python
# -*- coding:utf-8 -*-
#allisnone on 20200505
import datetime
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,Float,DateTime,PrimaryKeyConstraint


Base = declarative_base()

def create_sessionmaker(db='trader.db'):
    """
    param db: db name
    return: obj of sessionmaker 
    """
    engine = create_engine('sqlite:///' + db + '?check_same_thread=False', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

"""
class ZBase(Base):
    __tablename__ = 'zbase'
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
"""
class Modversion(Base):
    """use for mod maintenance"""
    __tablename__ = 'modversion'
    #id = Column(Integer, primary_key=True, autoincrement=True)
    mod = Column(String(32),unique=True,primary_key=True)
    version = Column(Integer,default=1)
    status = Column(Integer,default=0)
    valid = Column(Boolean,default=True) #1-valid, 0-invalid
    interval = Column(Integer,default=86400)  #update every interval, default one day
    value = Column(Float,default=None)  #if position, position value
    count = Column(Integer,default=3)
    max = Column(Float,default=0.8)  #if position, the max position rate
    fixtime =  Column(String(10), default=None) #fixed time to update data every date
    related = Column(String(256),default='') #related stocks 
    updatetime = Column(DateTime, default=datetime.datetime.now())
    endtime = Column(DateTime, default=None)
    nexttime = Column(DateTime, default=None) #next update time
    comment = Column(String(32),default='')
    #columns=['starttime','endtime', 'nexttime', 'status', 'valid','interval','value','count','max','update_time','comment']
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

class Orderevents(Base):
    """use for strategory ordering and trading"""
    __tablename__ = 'orderevents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(32),unique=True)  ## updatetime + stock
    #orderevent = Column(String(32))#,index=True)
    direction = Column(Integer,default=0) #0-buy, 1-sell
    ordertype = Column(Integer,default=0) #0-limit price
    stock = Column(String(6))
    price = Column(Float)
    volume = Column(Integer)
    valid = Column(Boolean,default=True) #1-valid, 0-invalid
    status = Column(Integer,default=0) #0-trigger, 1-sent order, 2-traded, 3-revised order, 4-canceled, 5-timeout,6-second-day-order
    strategyid = Column(String(32),default='033')  #011-t+0, 033-strategy33
    orderid = Column(String(32),default=None)
    tradeid = Column(String(32),default=None)
    starttime = Column(DateTime, default=None)
    delay = Column(Integer,default=300)
    interval = Column(Integer,default=60)
    count = Column(Integer,default=5)
    endtime = Column(DateTime,default=datetime.datetime.strptime(datetime.datetime.now().strftime('%Y%m%d')+'145959','%Y%m%d%H%M%S'))
    updatetime = Column(DateTime, default=datetime.datetime.now()) #datetime.datetime.utcnow()
    comment = Column(String(32),default='')
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Histfund(Base):
    """use for recording position and fund"""
    __tablename__ = 'histfund'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(32),unique=True)  # updatetime + account
    account = Column(String(32),default='abc123')
    market = Column(Float, nullable=False)
    capital = Column(Float, nullable=False)
    cash = Column(Float, default=0)
    position = Column(Float, default=None)
    updatetime = Column(DateTime, default=datetime.datetime.now())
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    """
    def __repr__(self):
        return "<Histfund(account='%s', updatetime='%s', market='%s', capital='%s', cash='%s', position='%s')>" % (self.account, self.updatetime, self.market, self.capital,self.cash,self.position)
    """

class Histstrategy33(Base):
    """use for recording Histstrategy33"""
    __tablename__ = 'histstrategy33'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #updatetime = Column(DateTime, default=datetime.datetime.now().date())
    uuid = Column(String(16),unique=True)  # updatetime + stock
    stock = Column(String(6),nullable=False)
    exit = Column(Float, nullable=False)
    buy = Column(Float, nullable=False)
    stop = Column(Float, default=-1) #stop profit, sell in high price, sell then buy in 0-3 dates;-1-disable
    trying = Column(Float, default=-1) ##try to buy, buy in low price, buy then sell in 0-n dates;-1-disable
    status = Column(Integer,default=-1) #0-buyed, 1-exited,2-stop,3-trying,-1-holding/unchanged
    tday = Column(Integer,default=1)
    ttarget = Column(Float, default=100.0)
    success = Column(Boolean,default=False)
    updatetime = Column(DateTime, default=datetime.datetime.now())
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    """"
    #sqlite not support
    __table_args__ = (
        PrimaryKeyConstraint('updatetime', 'stock'),
        {},
    )
    """





    