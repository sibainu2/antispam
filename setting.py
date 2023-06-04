
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
engine = create_engine('sqlite:///test.db', echo=False)

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

    def __init__(self, content, user,guild):
        if user is None:
            raise ValueError("ユーザー情報がNoneTypeです")
        if user.mute:
            raise ValueError('Cannot add message to muted user')
        self.content = content
        self.user = user
        self.guild = guild


#Base.metadata.drop_all(engine)
# テーブルを作成
Base.metadata.create_all(engine)

# データを追加
#or name in data.USER_NAMES:
#   user = User(name=name, mute=False, threat=0)
#   session.add(user)
#ession.commit()

# データを取得
#users = session.query(User).all()
#for user in users:
#    print(user.name, user.id)


from anti_spam_tool.event import on_message
@event.listens_for(Message, 'after_insert')
def on_new_message(mapper, connection, target):
    global loop, task
    if type(target) is Message:
        #print('New message added:', target.message)
        
        loop = asyncio.get_event_loop()
        task = loop.create_task(on_message(target))


#ここから下は荒らし
async def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def spam(number):
    guild = session.get(Guild,1)
    if guild is None:
        raise TypeError("guildが空だよ")
    user = session.get(User,number)
    
    for i in range(1,random.randint(5,10)):
        randomnam = await randomname(5)
        try:
            message = Message(content=f'こんにちわ日本語って入るの？{randomnam}', user=user,guild=guild)
            session.add(message)
            session.commit()
            await asyncio.sleep(random.uniform(0.5,1))
        except ValueError:
            print("書き込みに失敗しました。")
        



async def spam_main():
    spam_user = [1,2,3,4,5,6,7,8,9,10]
    tasks = [asyncio.create_task(spam(user_id)) for user_id in spam_user]
    await asyncio.gather(*tasks)
    print("タスクをすべて実行完了")

if __name__ == '__main__':
    asyncio.run(spam_main())
    



#loop.run_until_complete(task)

