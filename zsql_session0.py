#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import create_sessionmaker,Orderevents,Modversion,Histstrategy33,Histfund
from sqlalchemy.orm import sessionmaker
#Session = sessionmaker(bind=engine)
#db_session = Session()

sqlite_db = 'trader.db'
db_session = create_sessionmaker(sqlite_db)
nt = datetime.datetime.now()
mod_version = {'positions':[0,nt,None,None,0,1,60,10000.0,3,0.8,'15:01','002256,600345',''],
        'fund':[0,nt,None,None,0,1,60,10000.0,None,None,'15:01','',''],
        'strategy33':[0,nt,None,None,0,1,60,None,3,None,'15:01','',''],
        'hangqing':[0,nt,None,None,0,1,60,None,3,None,'14:01','',''],
        'traderapi':[0,nt,None,None,0,1,60,None,3,None,'14:01','',''],
        'kdata':[0,nt,None,None,0,1,60,None,3,None,'14:01','',''],
        'backtest':[0,nt,None,None,0,1,60,None,3,None,'14:01','',''],
        'report':[0,nt,None,None,0,1,60,None,3,None,'14:01','',''],
        'ipo':[0,nt,None,None,0,1,60,None,10,0.8,'13:10','',''],
        'tplus':[0,nt,None,None,0,0,60,None,10,0.8,'14:01','002236,300047',''],
        'daban':[0,nt,None,None,0,0,60,None,10,0.8,'9:25','002236,300047',''],
        'preorder':[0,nt,None,None,0,1,60,None,10,0.8,'18:00','002236,300047',''],
        'order':[0,nt,None,None,0,1,60,None,10,0.8,'18:00','002236,300047',''],
        'trade':[0,nt,None,None,0,0,60,None,10,0.8,'9:25','002236,300047',''],
        'dapan':[0,nt,None,None,0,0,60,None,10,0.8,'9:25','002236,300047',''],
        'potential':[0,nt,None,None,0,1,60,None,10,0.8,'14:01','002236,300047','']
        }
columns=['version','updatetime','endtime', 'nexttime', 'status', 'valid','interval','value','count','max','fixtime','related','comment']

def init_modversion(db_session):
    version = 0
    nt = datetime.datetime.now()
    #datetime.datetime.strptime(datetime.datetime.now().strftime('%Y%m%d')+'145959','%Y%m%d%H%M%S')
    capital = 10000.0
    market = 8000.0
    position_codes = ['300195','300716','600237']
    index_codes = ['600519','601318']
    starttime = '9:25'
    endtime = '15:01'
    kdatetime = '16:00'
    noontime = '13:10'
    ttime = '10:30'
    postclosetime = '14:40'
    mods = ['positions','fund','strategy33','hangqing','traderapi','kdata','backtest','report','ipo','tplus','dapan','order','preorder','trade','potential']
    for mod in mods:
        related = ''
        value = 0
        fixedtime = None
        if mod in ['positions','fund','strategy33']:
            related = ','.join(position_codes)
            value = capital
            fixedtime = endtime
        elif mod in ['kdata','backtest','report','potential']:
            fixedtime = kdatetime
        elif mod in ['tplus']:
            fixedtime = ttime
            value = market
        elif mod in ['ipo','order','trade']:
            fixedtime = noontime
            value = capital - market
        elif mod in ['preorder','traderapi']:
            fixedtime = starttime
            value = capital - market
        elif mod in ['postorder']:
            fixedtime = postclosetime
            value = capital - market
        elif mod=='dapan':
            related = ','.join(index_codes)
            fixedtime = kdatetime
        else:
            pass
        m = Modversion(mod=mod,version=version,updatetime=nt,endtime=None,nexttime=None, status=0, 
                valid=True,interval=60,value=value,count=3,max=0.8,fixtime=fixedtime,related=related,comment='')
        db_session.add(m)
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(e)
    return
#modversion
init_modversion(db_session)
      
class Handling_modversion:
    def __init__(self,db_session):
        self.db_session = db_session
        
    def add(self,mod_obj):
        try:
            if isinstance(mod_obj, list):
                self.db_session.add_all(mod_obj)
            else:
                self.db_session.add(mod_obj)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            print(e)
    
    def update(self,m_class,condition,datas={}):
        try:
            self.db_session.query(Orderevents).filter(Orderevents.id==2).update({"volume":400,'valid':False})
        except Exception as e:
            self.db_session.rollback()
            print(e)

#orderevent  
#add sql data
dt = datetime.datetime.now()
dt_str = dt.strftime('%Y%m%d')
dt_time_str = dt.strftime('%Y%m%d%H%M%S')
code='600123'
direction=0
orderuuid = dt_time_str + code + '%s'%direction
order1 = Orderevents(uuid=orderuuid,direction=0,ordertype=0,code=code,price=6.8,volume=100)  #buy
code='600124'
direction=1
orderuuid = dt_time_str + code + '%s'%direction
order2 = Orderevents(uuid=orderuuid,direction=direction,ordertype=0,code=code,price=9.8,volume=200) #sell
try:
    db_session.add(order1)
    db_session.add(order2)
    db_session.commit()
except Exception as e:
    db_session.rollback()
    print(e)


#histstrategy33

code='300712'
s33_1 = Histstrategy33(updatetime=dt,code='300712',uuid=dt_str+code,exit=4.08,buy=4.22,stop=4.76,trying=3.56)
code='600237'
s33_2 = Histstrategy33(updatetime=dt,code='300712',uuid=dt_str+code,exit=3.50,buy=3.82,stop=4.25,trying=3.59)
try:
    db_session.add(s33_1)
    db_session.add(s33_2)
    db_session.commit()
except Exception as e:
    db_session.rollback()
    print(e)

#histstrategy33
dt_str1 = '20200428'
account = 'abc01'
dt = datetime.datetime.strptime('20200428','%Y%m%d')
fund_1 = Histfund(uuid=dt_str1+account,account=account,updatetime=dt,market=8000.0,capital=10000.0)
account = 'abc02'
fund_2 = Histfund(uuid=dt_str+account,account=account,market=16000.0,capital=20000.0)
try:
    db_session.add(fund_1)
    db_session.add(fund_2)
    
    db_session.commit()
except Exception as e:
    db_session.rollback()
    print(e)
#update sql data
event = db_session.query(Orderevents).filter(Orderevents.id > 2).first()
res = db_session.query(Orderevents).filter(Orderevents.id==1).update({"status":1})
#print(event.id, event.code,event.volume)
res = db_session.query(Orderevents).filter(Orderevents.id==2).update({"volume":400,'valid':False})
print(res) # 1 res就是我们当前这句更新语句所更新的行数

db_session.commit()

#filter and query
event_all_list = db_session.query(Orderevents).filter(Orderevents.id >= 2).all()
print(event_all_list)
for i in event_all_list:
    print(i.id, i.code)

event = db_session.query(Orderevents).filter(Orderevents.id >= 3).first()
#print(event.id, event.code)

#delete:
db_session.query(Orderevents).filter(Orderevents.id == 1001).delete()

#order:
std_ord_desc = db_session.query(Orderevents).filter(Orderevents.code.like("%600%")).order_by(Orderevents.code.desc()).all()
for i in std_ord_desc:
  print(i.id)


#bool
event = db_session.query(Orderevents).filter(Orderevents.valid == False).first()
print(event.id, event.code)

#datetime
filter_time = datetime.datetime.strptime('20200505113720','%Y%m%d%H%M%S')
event = db_session.query(Orderevents).filter(Orderevents.updatetime >= filter_time).all()
print(event)
event = db_session.query(Orderevents).filter(Orderevents.updatetime >= filter_time).first()
print(event.id, event.code,event.updatetime)

db_session.close()


