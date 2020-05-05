#!/usr/bin/env python
# -*- coding:utf-8 -*-
#allisnone on 20200505
import datetime
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,Float,DateTime


Base = declarative_base()
class Modversion(Base):
    """use for mod maintenance"""
    __tablename__ = 'modversion'
    #id = Column(Integer, primary_key=True, autoincrement=True)
    mod = Column(String(32),unique=True)
    version = Column(Integer,default=1)
    updatetime = Column(DateTime, default=datetime.datetime.utcnow)
    endtime = Column(DateTime, default=None)
    endtime = Column(DateTime, default=None)
    status = Column(Integer,default=0)
    valid = Column(Boolean,default=True)
    interval = Column(Integer,default=None)
    count = Column(Integer,default=None)
    max = Column(Float,default=None)
    related = Column(String(256),default='')
    comment = Column(String(32),default='')
    #columns=['starttime','endtime', 'nexttime', 'status', 'valid','interval','value','count','max','update_time','comment']
    

class Orderevents(Base):
    """use for strategory ordering and trading"""
    __tablename__ = 'orderevents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #orderevent = Column(String(32))#,index=True)
    updatetime = Column(DateTime, default=datetime.datetime.now()) #datetime.datetime.utcnow()
    direction = Column(Integer,default=0) #0-buy, 1-sell
    ordertype = Column(Integer,default=0) #0-limit price
    stock = Column(String(6))
    price = Column(Float)
    volume = Column(Integer)
    valid = Column(Boolean,default=True)
    status = Column(Integer,default=0)
    strategyid = Column(String(32),default=None)
    orderid = Column(String(32),default=None)
    tradeid = Column(String(32),default=None)
    starttime = Column(DateTime, default=None)
    endtime = Column(DateTime,default=datetime.datetime.strptime(datetime.datetime.date(now).strftime('%Y%m%d')+'145959','%Y%m%d%H%M%S'))
    delay = Column(Integer,default=None)
    interval = Column(Integer,default=None)
    count = Column(Integer,default=None)
    comment = Column(String(32),default='')

class Histfund(Base):
    """use for recording position and fund"""
    __tablename__ = 'histfund'
    id = Column(Integer, primary_key=True, autoincrement=True)
    updatetime = Column(DateTime, default=datetime.datetime.date(now))
    market = Column(Float, default=None)
    capital = Column(Float, default=None)
    position = Column(Float, default=None)

class Histstrategy33(Base):
    """use for recording Histstrategy33"""
    __tablename__ = 'histstrategy33'
    id = Column(Integer, primary_key=True, autoincrement=True)
    updatetime = Column(DateTime, default=datetime.datetime.date(now))
    stock = Column(String(6))
    exit = Column(Float, default=None)
    buy = Column(Float, default=None)
    stop = Column(Float, default=None) #stop profit, sell in high price, sell then buy in 0-3 dates
    trying = Column(Float, default=None) ##try to buy, buy in low price, buy then sell in 0-n dates
    status = Column(Integer) #0-buy, 1-exit,2-stop,3-trying,-1-holding/unchanged
    success = Column(Boolean,default=False)
     
sqlite_db = 'test.db'
engine = create_engine('sqlite:///' + sqlite_db + '?check_same_thread=False', echo=False)
Base.metadata.create_all(engine)
