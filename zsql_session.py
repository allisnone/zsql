#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import engine,Orderevents,Modversion
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
db_session = Session()
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
    position_stocks = ['300195','300716','600237']
    index_stocks = ['600519','601318']
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
            related = ','.join(position_stocks)
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
            related = ','.join(index_stocks)
            fixedtime = kdatetime
        else:
            pass
        m = Modversion(mod=mod,version=version,updatetime=nt,endtime=None,nexttime=None, status=0, 
                valid=True,interval=60,value=value,count=3,max=0.8,fixtime=fixedtime,related=related,comment='')
        db_session.add(m)
    db_session.commit()
    return

init_modversion(db_session)        
#add sql data
order1 = Orderevents(stock='600123',price=6.8,volume=100)
order2 = Orderevents(stock='600124',price=9.8,volume=200)

#db_session.add(order1)
#db_session.add(order2)
db_session.commit()

#update sql data
event = db_session.query(Orderevents).filter(Orderevents.id >= 2).first()
print(event.id, event.stock,event.volume)
res = db_session.query(Orderevents).filter(Orderevents.id==2).update({"volume":400,'valid':False})
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


