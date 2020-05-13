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
    position_s = ['300195','300716','600237']
    index_s = ['600519','601318']
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
            related = ','.join(position_s)
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
            related = ','.join(index_s)
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
    def __init__(self,db_session,model=None,logger=None):
        self.db_session = db_session
        self.logger = logger
        self.model = model
        
    def set_model(self,model):
        self.model = model   
            
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
        param datas: dict type, update field data
        return: none
        """
        return
    
    def delete(self,filter,by_id=False):
        """
        param filter: filter unique Column or key id
        param datas: dict type, update field data
        return: none
        """
        return
    
    def set_filter_column(self,column):
        """
        param column:  Column type, like Histstrategy33.uuid
        return: none
        """
        self.filer_column = column 
    
    def _is_updated(self,filter,baseline,by_id=False,by_uuid=False):
        """
        param filter: filter value for unique Column
        param baseline: dict type, update field data
        param by_id: bool
        return: Bool or None
        """
        if by_id:
            self.set_filter_column(self.model.id)
        if by_uuid:
            self.set_filter_column(self.model.uuid)
        try:
            filter_obj = self.db_session.query(self.model).filter(self.filer_column==filter).first()
            return filter_obj.updatetime>=baseline
        except Exception as e:
            if self.logger: self.logger.info(e)
        return None
    
    def get_filter_objects(self,filter=None,basetime=None,opt='gte',by_id=False,by_updatetime=False,filter_column=None):
        """
        param filter: filter value by unique Column
        param basetime: datetime type, use for filter data by time
        param opt: str type, use for filter data by time
        param by_id: bool type, default: False
        param by_updatetime: bool type, default: False
        param filter_column, Column object, like Histstrategy33.uuid
        return: sqlalchemy.orm.query.Query or None
        """
        try:
            #filter_obj = self.db_session.query(self.model).filter(self.model.uuid>=filter).first()
            filter_obj = None
            if by_updatetime:
                if opt=='gt':
                    filter_obj = self.db_session.query(self.model).filter(self.model.updatetime>basetime)
                elif opt=='gte':
                    filter_obj = self.db_session.query(self.model).filter(self.model.updatetime>=basetime)
                elif opt=='eq':
                    filter_obj = self.db_session.query(self.model).filter(self.model.updatetime==basetime)
                else:#lt
                    filter_obj = self.db_session.query(self.model).filter(self.model.updatetime<basetime)
            else:#by uuid or by id
                #key = self.model.uuid  #or others
                if by_id:
                    filter_column = self.model.id
                if opt=='gt':
                    filter_obj = self.db_session.query(self.model).filter(filter_column>filter)
                elif opt=='gte':
                    filter_obj = self.db_session.query(self.model).filter(filter_column>=filter)
                elif opt=='eq':
                    filter_obj = self.db_session.query(self.model).filter(filter_column==filter)
                else:#lt
                    filter_obj = self.db_session.query(self.model).filter(filter_column<filter)
            return filter_obj  
        except Exception as e:
            if self.logger: self.logger.info(e)
        return None
    
    def close(self):
        self.db_session.close()
        return
                  
class Handle_modversion(Basehandle):
    """handle method for modversion"""
    def __init__(self,db_session,logger=None):
        super(Handle_modversion,self).__init__(db_session,logger)
        self.model = Modversion

    def update(self,filter,datas):
        """
        param filter: str, mod name
        param datas: dict type, update field data
        return: none
        """
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.mod==filter)
            #print(this_mod.first().version)
            datas['version'] = filter_obj.first().version + 1
            filter_obj.update(datas)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
            else: print(e)
        return False
    
    def delete(self,filter): #delete filter by mod
        """
        param filter: str, mod name
        return: none
        """
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.mod==filter).delete()
            self.db_session.commit()
            return True
        except Exception as e:
            if self.logger: self.logger.info(e)
        return False
    
    def is_updated(self,filter,baseline):
        """
        param filter: filter value for unique Column
        param baseline: dict type, update field data
        return: Bool or None
        """
        self.set_filter_column(self.model.mod)
        return self._is_updated(filter, baseline)

class Handle_model(Basehandle):
    """
    model can be Histfund, Histstrategy33, Orderevents
    """
    def __init__(self,db_session,model,logger=None):
        super(Handle_model,self).__init__(db_session,logger)
        self.model = model
        
    def add_table_objects(self,obj):
        """
        param obj: object from Class: Base = declarative_base()
        return: none
        """
        add_num = self.add(obj)
        if add_num>0:# update mod updatetime
            h = Handle_modversion(self.db_session,self.logger)
            if self.model.__tablename__=='histstrategy33':
                h.update(filter='strategy33', datas={'updatetime':datetime.datetime.now()})
            elif self.model.__tablename__=='histfund':
                h.update(filter='fund', datas={'updatetime':datetime.datetime.now()}) 
            elif self.model.__tablename__=='orderevents':
                h.update(filter='order', datas={'updatetime':datetime.datetime.now()}) 
            #should add more, if more models
            else:
                if self.logger: self.logger.info('add_and_update_realted_mod-added {0} rows for table={1} with mod update'.format(add_num,self.model.__tablename__))
        else:
            if self.logger: self.logger.info('add_and_update_realted_mod-Nothing will be add to table={0}'.format(self.model.__tablename__))
        
        return
    
    def update(self,filter,datas={},by_id=False):
        """
        param filter: filter unique Column
        param datas: dict type, update field data
        param by_id: bool
        return: none
        """
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.uuid==filter)
            #print(this_mod.first().version)
            filter_obj.update(datas)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            if self.logger: self.logger.info(e)
    
    def delete(self,filter,by_id=False):
        """
        param filter: filter unique Column
        param by_id: bool
        return: none
        """
        try:
            filter_obj = self.db_session.query(self.model).filter(self.model.uuid==filter).delete()
            self.db_session.commit()
        except Exception as e:
            if self.logger: self.logger.info(e)
        return
    
    def is_updated(self,filter,baseline,by_id=False,by_uuid=False):
        """
        param filter: filter value for unique Column
        param baseline: dict type, update field data
        param by_id: bool
        param by_uuid: bool
        return: Bool or None
        """
        #to do
        #self.set_filter_column(column=self.model.uuid)
        return self._is_updated(filter, baseline, by_id, by_uuid)
    
    #filter by updatettime
    def get_filter_objects_by_updatetime(self,basetime,opt='gte'):
        """
        param basetime: datetime type, use for filter data by time
        param opt: str type, use for filter data by time
        return: sqlalchemy.orm.query.Query or None
        """
        return self.get_filter_objects(basetime=basetime,opt=opt,by_updatetime=True)
    
    #filter by table column
    def get_filter_objects_by_column(self,filter,column,opt='eq'):
        """
        param filter: filter value by unique Column
        param column, Column object, like Histstrategy33.uuid
        param opt: str type, use for filter data by time
        return: sqlalchemy.orm.query.Query or None
        """
        #get_filter_objects_by_column(self,filter='304749',column=Orderevents.code,opt='eq')
        #get_filter_objects_by_column(self,filter='20200428051213305748',column=Orderevents.uuid,opt='eq')
        return self.get_filter_objects(filter=filter,opt=opt,filter_column=column)
    
    #filter by id
    def get_filter_objects_by_id(self,id,opt='eq'):
        """
        param id: int
        param opt: str type, use for filter data by time
        return: sqlalchemy.orm.query.Query or None
        """
        return self.get_filter_objects(filter=id,opt=opt,by_id=True)
    
        