
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, event
import datetime
import asyncio
import data
import random
import string

# create_engine関数でエンジンを作成
engine = create_engine('sqlite:///test.db', echo=True)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

# テーブルを作成するためのベースクラスを作成
Base = declarative_base()

# テーブルの定義
class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    users = relationship("User", back_populates="guild",)
    messages = relationship("Message", back_populates="guild")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    mute = Column(Boolean,default=False)#発言権
    threat = Column(Integer,default=0)#脅威
    messages = relationship("Message", back_populates="user")
    guild_id = Column(Integer, ForeignKey('guilds.id'))
    guild = relationship("Guild", back_populates="users")
    def __init__(self,name ,guild ,mute=False,threat=0):
        if guild is None:
            raise ValueError("サーバー情報がNoneTypeです")
        self.name = name
        self.guild = guild
        self.mute = mute
        self.threat = threat

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String,nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="messages")
    guild_id = Column(Integer, ForeignKey('guilds.id'))
    guild = relationship("Guild", back_populates="messages")

    def __init__(self, content, user):
        if user is None:
            raise ValueError("ユーザー情報がNoneTypeです")
        if user.mute:
            raise ValueError('Cannot add message to muted user')
        self.content = content
        self.user = user



Base.metadata.drop_all(engine)
# テーブルを作成
Base.metadata.create_all(engine)

# データを追加
guild = Guild(name="test")
session.add(guild)
session.commit()

for name in data.USER_NAMES:
    user = User(name=name,guild=guild)
    session.add(user)
session.commit()

# データを取得
