import sys
sys.path.append('../')
import time
import asyncio
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
import MeCab



#Classのidについて
#UserクラスとメッセージクラスにあるIDはdiscordのIDを使用してください。
#wordクラスにあるIDは単語の順番どおりにIDを振ってください

class User():
    def __init__(self,id:int,name:str,bot:bool,mute:bool=False,threat:float=0,messages:list=[]) -> None:
        self.id = id
        self.name = name
        self.bot = bot
        self.mute = mute
        self.threat = threat
        self.messages = messages#messageのIDのリストです。

    def add_message(self,message_id:int):
        self.message.append(message_id)

    def silence(self):
        self.mute = True

    def unsilence(self):
        self.mute = False

class Word():
    def __init__(self,id:int,word:str,yomi:str,top:int,end:int,):
        self.id = id
        self.word = word
        self.yomi = yomi 
        self.top = top
        self.end = end
        

    def __add__(self,other):
        if type(other) != Word:
            raise TypeError(f"同じクラスではありません。[{other.word}:{type(other)}]")
        if (self.end +1 - other.top) != 0:
            raise ValueError(f"単語が連続した順番ではありません。[({self.word,self.top,self.end},{other.word,other.top,other.end})]")
    
        return Word(id=None,word=self.word+other.word,top=self.top,end=other.end)
    
    def __eq__(self,other):
        if type(other) != Word:
            raise TypeError(f"同じクラスではありません。[{other.word}:{type(other)}]")
        
        return self.word == other.word and self.yomi == self.yomi

class Message():
    def __init__(self,id:int,content:str,user:User,delete:bool,guild:int):
        self.id = id
        self.content = content
        self.user = user#userのIDです。
        self.delete = delete
        self.guild = guild


    def clear(self):
        self.user.messages.pop(self.id)

class TmpGuild():
    def __init__(self,id):
        self.id = id
        self.messages:list[Message] = []
        self.users:list[User] = []

        self.spam_messages:list[Message] = []
        self.spam_users:list[User] = []


def analyze_text(text):
    # MeCabの初期化
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

    # テキストを形態素解析して結果を取得
    node = m.parseToNode(text)

    # 分解した内容、分解した意味、および読みを格納するリスト
    morphemes = []
    meanings = []
    readings = []

    while node:
        surface = node.surface
        feature = node.feature.split(",")
        morpheme = surface
        meaning = feature[0]
        reading = feature[7] if len(feature) > 7 else ""
        morphemes.append(morpheme)
        meanings.append(meaning)
        readings.append(reading)
        node = node.next

    # 先頭ノードは空なので削除
    morphemes = morphemes[1:]
    meanings = meanings[1:]
    readings = readings[1:]
    output = list(zip(morphemes, meanings, readings))

    if output and output[-1] == ('', 'BOS/EOS', '*'):
        output.pop()  # リストの最後の要素を削除

    return output

tmp_message:list[TmpGuild] = []

async def on_message(message):
    global tmp_message
    
    if message.guild.id not in [guild.id for guild in tmp_message]:#一時保存場所にギルドデータがない場合は追加する。
        tmp_message.append(TmpGuild(id=message.guild.id))

    user = message.user
    print(message.id,user.name,analyze_text(message.content))



