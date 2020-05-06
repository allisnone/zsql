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
    mod = Column(String(32),unique=True,primary_key=True)
    version = Column(Integer,default=1)
    updatetime = Column(DateTime, default=datetime.datetime.utcnow)
    endtime = Column(DateTime, default=None)
    nexttime = Column(DateTime, default=None) #next update time
    status = Column(Integer,default=0)
    valid = Column(Boolean,default=True) #1-valid, 0-invalid
    interval = Column(Integer,default=86400)  #update every interval, default one day
    value = Column(Float,default=None)  #if position, position value
    count = Column(Integer,default=3)
    max = Column(Float,default=0.8)  #if position, the max position rate
    fixtime =  Column(String(10), default=None) #fixed time to update data every date
    related = Column(String(256),default='') #related stocks 
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
    valid = Column(Boolean,default=True) #1-valid, 0-invalid
    status = Column(Integer,default=0) #0-trigger, 1-sent order, 2-traded, 3-revised order, 4-canceled, 5-timeout,6-second-day-order
    strategyid = Column(String(32),default=None)
    orderid = Column(String(32),default=None)
    tradeid = Column(String(32),default=None)
    starttime = Column(DateTime, default=None)
    endtime = Column(DateTime,default=datetime.datetime.strptime(datetime.datetime.now().strftime('%Y%m%d')+'145959','%Y%m%d%H%M%S'))
    delay = Column(Integer,default=300)
    interval = Column(Integer,default=60)
    count = Column(Integer,default=5)
    comment = Column(String(32),default='')

class Histfund(Base):
    """use for recording position and fund"""
    __tablename__ = 'histfund'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(32),default='')
    updatetime = Column(DateTime, default=datetime.datetime.now())
    market = Column(Float, default=0)
    capital = Column(Float, nullable=False)
    cash = Column(Float, default=0)
    position = Column(Float, default=None)

class Histstrategy33(Base):
    """use for recording Histstrategy33"""
    __tablename__ = 'histstrategy33'
    id = Column(Integer, primary_key=True, autoincrement=True)
    updatetime = Column(DateTime, default=datetime.datetime.now())
    stock = Column(String(6))
    exit = Column(Float, nullable=False)
    buy = Column(Float, nullable=False)
    stop = Column(Float, default=-1) #stop profit, sell in high price, sell then buy in 0-3 dates
    trying = Column(Float, default=-1) ##try to buy, buy in low price, buy then sell in 0-n dates
    status = Column(Integer,default=-1) #0-buy, 1-exit,2-stop,3-trying,-1-holding/unchanged
    success = Column(Boolean,default=False)
     
sqlite_db = 'test.db'
engine = create_engine('sqlite:///' + sqlite_db + '?check_same_thread=False', echo=False)
Base.metadata.create_all(engine)

    