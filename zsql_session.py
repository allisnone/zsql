#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import engine,Orderevents,Modversion
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
db_session = Session()

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

def init_modversion():
    version = 0
    nt = datetime.datetime.now()
    capital = 10000.0
    position_stocks = ['300195','300716','600237']
    index_stocks = ['600519','601318']
    starttime = '9:25'
    endtime = '15:01'
    kdatetime = '16:00'
    noontime = '13:10'
    mods = ['positons','fund','strategy33','hangqing','traderapi','kdate','backtest','report','ipo','tplus','dapan','order','preorder','trade','potential']
    for mod in mods:
        related = ''
        value = 0
        
        if mod in ['positions','fund','strategy33','tplus','preorder','trade']:
            related = ','.join(position_stocks)
            value = capital
        elif mod=='dapan':
            related = ','.join(index_stocks)
        else:
            pass
        fixedtime = None
        
        m = Modversion(mod=mod,version=version,updatetime=nt,endtime=None,nexttime=None, status=0, 
                valid=True,interval=60,value=value,count=3,max=0.8,fixtime=fixedtime,related=related,comment='')
        
        db_session.add(m)
#add sql data
order1 = Orderevents(stock='600123',price=6.8,volume=100)
order2 = Orderevents(stock='600124',price=9.8,volume=200)

#db_session.add(order1)
#db_session.add(order2)
db_session.commit()

#update sql data
event = db_session.query(Orderevents).filter(Orderevents.id >= 3).first()
print(event.id, event.stock,event.volume)
res = db_session.query(Orderevents).filter(Orderevents.id==9).update({"volume":400,'valid':False})
print(res) # 1 res就是我们当前这句更新语句所更新的行数

db_session.commit()

#filter and query
event_all_list = db_session.query(Orderevents).filter(Orderevents.id >= 2).all()
print(event_all_list)
for i in event_all_list:
    print(i.id, i.stock)

event = db_session.query(Orderevents).filter(Orderevents.id >= 3).first()
print(event.id, event.stock)

#delete:
db_session.query(Orderevents).filter(Orderevents.id == 1001).delete()

#order:
std_ord_desc = db_session.query(Orderevents).filter(Orderevents.stock.like("%600%")).order_by(Orderevents.stock.desc()).all()
for i in std_ord_desc:
  print(i.id)


#bool
event = db_session.query(Orderevents).filter(Orderevents.valid == False).first()
print(event.id, event.stock)

#datetime
filter_time = datetime.datetime.strptime('20200505113720','%Y%m%d%H%M%S')
event = db_session.query(Orderevents).filter(Orderevents.updatetime >= filter_time).all()
print(event)
event = db_session.query(Orderevents).filter(Orderevents.updatetime >= filter_time).first()
print(event.id, event.stock,event.updatetime)

db_session.close()


