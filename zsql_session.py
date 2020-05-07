#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import create_sessionmaker,Orderevents,Modversion,Histstrategy33,Histfund
from zhandle import init_modversion,Handle_modversion,Handle_model

sqlite_db = 'trader.db'
db_session = create_sessionmaker(sqlite_db)
nt = datetime.datetime.now()
#modversion
#init_modversion(db_session)

hm = Handle_modversion(db_session)
#updatae modversion data
#hm.update_modversion_by_mod('kdata', datas={'status':0})

#is mod update
dt = datetime.datetime.now()
dt = datetime.datetime.strptime('20200505141300','%Y%m%d%H%M%S')
is_update = hm.is_updated(filter='kdata', baseline=dt)
print(is_update)

#orderevent  
#add sql data
#dt = datetime.datetime.now()
dt_str = dt.strftime('%Y%m%d')
dt_time_str = dt.strftime('%Y%m%d%H%M%S')
stock='600123'

#------------------------------------------------------Histstrategy33
hm = Handle_model(db_session,model=Histstrategy33,logger=None)
hm.update(filter='20200506300712', datas={'status':2})
stra_updated = hm.is_updated(filter='20200507300712',baseline=dt)
print('stra_updated=',stra_updated)

dt_str1 = '20200428'
stock='305729'
s33_1 = Histstrategy33(updatetime=dt,stock=stock,uuid=dt_str1+stock,exit=4.08,buy=4.22,stop=4.76,trying=3.56)
stock='305730'
s33_2 = Histstrategy33(updatetime=dt,stock=stock,uuid=dt_str1+stock,exit=4.08,buy=4.22,stop=4.76,trying=3.56)
hm.add_and_update_realted_mod(obj=[s33_1,s33_2])

baseline = datetime.datetime.strptime('20200506150000','%Y%m%d%H%M%S')
obj = hm.get_filter_objects(filter,baseline,opt='lt',by_id=False,by_updatetime=True)
for o in obj:
    print(o.to_dict())
print('----------')
filter = '20200428306729'
obj = hm.get_filter_objects(filter,baseline,opt='eq',by_id=False,by_updatetime=False,filter_key=Histstrategy33.uuid)
for o in obj:
    print(o.to_dict())

#------------------------------------------------------Histfund
hm.set_model(model=Histfund)
hm.update(filter='20200428abc01', datas={'position':0.6})

fund_updated = hm.is_updated(filter='20200428abc01',baseline=dt)
print('fund_updated=',fund_updated)

account = 'abc57'
dt = datetime.datetime.strptime('20200428','%Y%m%d')
fund_1 = Histfund(uuid=dt_str1+account,account=account,updatetime=dt,market=8000.0,capital=10000.0)
account = 'abc58'
fund_2 = Histfund(uuid=dt_str1+account,account=account,updatetime=dt,market=8000.0,capital=10000.0)
hm.add_and_update_realted_mod([fund_1,fund_2])

#------------------------------------------------------Orderevents
hm.set_model(model=Orderevents)
direction=0
orderuuid = dt_time_str + stock + '%s'%direction
order1 = Orderevents(uuid=orderuuid,direction=0,ordertype=0,stock=stock,price=6.8,volume=100)  #buy

dt_str1 = '20200428051213'
stock='305748'
order1 = Orderevents(uuid=dt_str1+stock,direction=0,ordertype=0,stock=stock,price=6.8,volume=100)  #buy
stock='305749'
order2 = Orderevents(uuid=dt_str1+stock,direction=0,ordertype=0,stock=stock,price=6.8,volume=100) 
hm.add_and_update_realted_mod([order1,order2])


db_session.close()

 