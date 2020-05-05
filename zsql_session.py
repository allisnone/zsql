#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from zmodels import engine,Orderevents
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
db_session = Session()

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


