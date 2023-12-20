"""
This module provides functionality for interacting with the database.
"""

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
engine = create_engine("sqlite:///local_database.db", echo=False)

# 创建一个基类
Base = declarative_base()


# 定义User模型
class User(Base):
    """
    Represents a user in the database.
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    score = Column(Integer, default=0)


# 创建表格
Base.metadata.create_all(engine)

# 创建Session类
Session = sessionmaker(bind=engine)


def insert_user(user_id, user_name):
    """
    Inserts a new user into the database.

    Args:
        user_id (int): The ID of the user.
        user_name (str): The name of the user.
    """
    session = Session()
    user = User(id=user_id, name=user_name)
    session.add(user)
    session.commit()
    session.close()


def delete_user(user_id):
    """
    Deletes a user from the database.

    Args:
        user_id (int): The ID of the user.
    """
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
    session.close()


def get_all_users():
    """
    Retrieves all users from the database.

    Returns:
        list: A list of User objects representing all users.
    """
    session = Session()
    users = session.query(User).all()
    session.close()
    return users


def update_user_name(user_id, new_name):
    """
    Updates the name of a user in the database.

    Args:
        user_id (int): The ID of the user.
        new_name (str): The new name of the user.
    """
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.name = new_name
        session.commit()
    session.close()


def update_or_insert_user(user_id, new_name):
    """
    Updates or inserts a user into the database.

    Args:
        user_id (int): The ID of the user.
        new_name (str): The new name of the user.
    """
    session = Session()
    user = User(id=user_id, name=new_name)
    session.merge(user)
    session.commit()
    session.close()


def update_user_score(user_id, score):
    """
    Updates the score of a user in the database.

    Args:
        user_id (int): The ID of the user.
        score (int): The new score of the user.
    """
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.score = score
        session.commit()
    session.close()


def get_user_score(user_id):
    """
    Retrieves the score of a user from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int: The score of the user.
    """
    session = Session()
    user = session.query(User).get(user_id)
    score = user.score if user else None
    session.close()
    return score


def get_user_name_by_id(user_id):
    """
    Retrieves the name of a user from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The name of the user.
    """
    session = Session()
    user = session.query(User).get(user_id)
    name = user.name if user else None
    session.close()
    return name
