#!/usr/bin/env python
# -*- coding:utf-8 -*-
#allisnone on 20200505
import datetime
from zmodels import Modversion

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

class Basehandle:
    """db base handle method """
    def __init__(self,db_session,logger=None):
        self.db_session = db_session
        self.logger = logger
        
    def add(self,obj):
        """
        param obj: table object
        return: none
        """
        try:
            if isinstance(obj, list):
                self.db_session.add_all(obj)
                self.db_session.commit()
                return len(obj)
            else:
                self.db_session.add(obj)
                self.db_session.commit()
                return 1
        except Exception as e:
            self.db_session.rollback()
            print(e)
            if self.logger: self.logger.info(e)
        return 0
        
    def update(self,filter,datas,by_id=False):
        """
        param filter: filter unique Column or key id
        param data: dict type, update field data
        return: none
        """
        return
    
    def delete(self,filter,by_id=False):
        """
        param filter: filter unique Column or key id
        param data: dict type, update field data
        return: none
        """
        return
    
    def is_updated(self,filter,baseline):
        """
        param filter: filter unique Column
        param data: dict type, update field data
        return: none
        """
        return
    
    def close(self):
        self.db_session.close()
        return
                  
class Handle_modversion(Basehandle):
    """handle method for modversion"""
    def __init__(self,db_session,logger=None):
        super(Handle_modversion,self).__init__(db_session,logger)

    def update(self,filter,datas={}):
        try:
            filter_obj = self.db_session.query(Modversion).filter(Modversion.mod==filter)
            #print(this_mod.first().version)
            datas['version'] = filter_obj.first().version + 1
            filter_obj.update(datas)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
            else: print(e)
    
    def delete(self,filter):
        try:
            filter_obj = self.db_session.query(Modversion).filter(Modversion.mod==filter).delete()
            self.db_session.commit()
        except Exception as e:
            if self.logger: self.logger.info(e)
        return
    
    def is_updated(self,filter,baseline):
        try:
            filter_obj = self.db_session.query(Modversion).filter(Modversion.mod==filter).first()
            return filter_obj.updatetime>=baseline
        except Exception as e:
            if self.logger: self.logger.info(e)
        return

class Handle_model(Basehandle):
    """
    model can be Histfund, Histstrategy33, Orderevents
    """
    def __init__(self,db_session,model,logger=None):
        super(Handle_model,self).__init__(db_session,logger)
        self.model = model
    
    def set_model(self,model):
        self.model = model
        
    def add_and_update_realted_mod(self,obj):
        add_num = self.add(obj)
        if add_num>0:# update mod updatetime
            h = Handle_modversion(self.db_session,self.logger)
            if self.model.__tablename__=='histstrategy33':
                h.update(filter='strategy33', datas={'updatetime':datetime.datetime.now()})
            elif self.model.__tablename__=='histfund':
                h.update(filter='fund', datas={'updatetime':datetime.datetime.now()}) 
            elif self.model.__tablename__=='orderevents':
                h.update(filter='order', datas={'updatetime':datetime.datetime.now()}) 
            else:
                if self.logger: self.logger.info('add_and_update_realted_mod-added {0} rows for table={1} with mod update'.format(add_num,self.model.__tablename__))
        else:
            if self.logger: self.logger.info('add_and_update_realted_mod-Nothing will be add to table={0}'.format(self.model.__tablename__))
        
        return
    
    def update(self,filter,datas={},by_id=False):
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.uuid==filter)
            #print(this_mod.first().version)
            filter_obj.update(datas)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
    
    def delete(self,filter,by_id=False):
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.uuid==filter).delete()
            self.db_session.commit()
        except Exception as e:
            if self.logger: self.logger.info(e)
        return
    
    def is_updated(self,filter,baseline):
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.uuid==filter).first()
            return filter_obj.updatetime>=baseline
        except Exception as e:
            if self.logger: self.logger.info(e)
        return