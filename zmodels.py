#!/usr/bin/env python
# -*- coding:utf-8 -*-
#allisnone on 20200505
import datetime
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,Float,DateTime


Base = declarative_base()
class Modversion(Base):
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
    

class Histfund(Base):
    __tablename__ = 'histfund'
    id = Column(Integer, primary_key=True, autoincrement=True)
    updatetime = Column(DateTime, default=datetime.datetime.date())
    market = Column(Float, default=None)
    capital = Column(Float, default=None)
    position = Column(Float, default=None)
    
class Orderevents(Base):
    __tablename__ = 'orderevents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #orderevent = Column(String(32))#,index=True)
    updatetime = Column(DateTime, default=datetime.datetime.utcnow)
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
    endtime = Column(DateTime,default=None)
    delay = Column(Integer,default=None)
    interval = Column(Integer,default=None)
    count = Column(Integer,default=None)
    comment = Column(String(32),default='')

     
columns=['starttime','endtime', 'nexttime', 'status', 'valid','interval','value','count','max','update_time','comment']
sqlite_db = 'test.db'
engine = create_engine('sqlite:///' + sqlite_db + '?check_same_thread=False', echo=False)
Base.metadata.create_all(engine)
