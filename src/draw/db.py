from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
engine = create_engine('sqlite:///local_database.db', echo=False)

# 创建一个基类
Base = declarative_base()


# 定义User模型
class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    score = Column(Integer, default=0)


# 创建表格
Base.metadata.create_all(engine)

# 创建Session类
Session = sessionmaker(bind=engine)


def insert_user(user_id, user_name):
    # 插入数据
    session = Session()
    user = User(id=user_id, name=user_name)
    session.add(user)
    session.commit()
    session.close()


def delete_user(user_id):
    # 删除数据
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
    session.close()


def get_all_users():
    # 获取所有用户数据
    session = Session()
    users = session.query(User).all()
    session.close()
    return users


def update_user_name(user_id, new_name):
    # 更新用户姓名
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.name = new_name
        session.commit()
    session.close()


def update_or_insert_user(user_id, new_name):
    # 使用 merge() 方法，如果用户存在则更新，不存在则插入新记录
    session = Session()
    user = User(id=user_id, name=new_name)
    session.merge(user)
    session.commit()
    session.close()


def update_user_score(user_id, score):
    # 更新用户分数
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.score = score
        session.commit()
    session.close()


def get_user_score(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    score = user.score if user else None
    session.close()
    return score


def get_user_name_by_id(user_id):
    # 使用查询语句查询用户姓名
    session = Session()
    user = session.query(User).get(user_id)
    name = user.name if user else None
    session.close()
    return name
