from sqlalchemy import DateTime
import datetime
class User():
    def __init__(self,id,name,mute,message_count,threat_level) -> None:
        self.id = id
        self.name = name
        self.mute = mute
        self.message_count = message_count
        self.threat_level = threat_level

class Message():
    def __init__(self,id:int,user:User,content:str,threat_level) -> None:
        self.id = id
        self.user = user
        self.content = content
        self.threat_level = threat_level

class SpamSession():
    def __init__(self) -> None:
        send_all_user = []
        mute_user = []
        all_message = []
        start_time:DateTime = datetime.datetime.utcnow()
        latest_time:DateTime = datetime.datetime.utcnow()
        end_time:DateTime = None