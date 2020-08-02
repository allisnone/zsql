from sqlalchemy import create_engine,Column,Integer,String,Boolean,Float,DateTime,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('mysql+pymysql://root:1234@localhost/test?charset=utf8', echo=False)
# engine = create_engine('sqlite:////MyDB.sqlite3', echo=False)
db='test.db'
engine = create_engine('sqlite:///' + db + '?check_same_thread=False', echo=False)

DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()
#定义类
class table_class(Base):
    __tablename__ = 'aaa'
    id=Column(Integer,primary_key=True)


# 动态添加字段
for i in range(3):
    setattr(table_class,'Col'+str(i),(Column('Col'+str(i), String(50))))
setattr(table_class,'Col3',(Column('Col3', String(50))))
Base.metadata.create_all(engine)

# 添加数据
dt=table_class(Col1='aaa',Col2="aaa")
session.add(dt)
session.commit()
session.close_all()

#如果有添加或者改变原表字段时，需要删除原有的数据表格
#Base.metadata.create_all(engine)
dt=table_class(Col1='aa3',Col2="aa3",Col3="ac3")
session.add(dt)
session.commit()
