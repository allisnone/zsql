#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import engine,Orderevents,Modversion,Histstrategy33,Histfund
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
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(e)
    return
#modversion
#init_modversion(db_session)
      
class Handling_model:
    def __init__(self,db_session,logger=None):
        self.db_session = db_session
        self.logger = logger
        
    def add(self,obj):
        try:
            if isinstance(obj, list):
                self.db_session.add_all(obj)
            else:
                self.db_session.add(obj)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
    
    def update_modversion_by_mod(self,mod,datas={}):
        try:
            filter = self.db_session.query(Modversion).filter(Modversion.mod==mod)
            #print(this_mod.first().version)
            datas['version'] = filter.first().version + 1
            filter.update(datas)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
    
    def is_mod_update(self,mod,baseline):
        try:
            filter = self.db_session.query(Modversion).filter(Modversion.mod==mod).first()
            return filter.updatetime>=baseline
        except Exception as e:
            if self.logger: self.logger.info(e)
        return


hm = Handling_model(db_session)
#updatae modversion data
#hm.update_modversion_by_mod('kdata', datas={'status':0})

#is mod update
dt = datetime.datetime.now()
dt = datetime.datetime.strptime('20200505141300','%Y%m%d%H%M%S')
is_update = hm.is_mod_update(mod='kdata', baseline=dt)
print(is_update)

#orderevent  
#add sql data
dt = datetime.datetime.now()
dt_str = dt.strftime('%Y%m%d')
dt_time_str = dt.strftime('%Y%m%d%H%M%S')
stock='600123'
direction=0
orderuuid = dt_time_str + stock + '%s'%direction
order1 = Orderevents(orderuuid=orderuuid,direction=0,ordertype=0,stock=stock,price=6.8,volume=100)  #buy
