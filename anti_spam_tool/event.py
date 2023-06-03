import sys
sys.path.append('../')
import time
import asyncio
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean



async def list_del(tmp_list):
    return [message.time for message in tmp_list]

tmp_message = []

async def on_message(message):
    global tmp_message

    user = message.user



