import threading

from sqlalchemy import Column, String

from HinataRobot.modules.sql import BASE, SESSION


class HinataChats(BASE):
    __tablename__ = "hinata_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


HinataChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_hinata(chat_id):
    try:
        chat = SESSION.query(HinataChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_hinata(chat_id):
    with INSERTION_LOCK:
        hinatachat = SESSION.query(HinataChats).get(str(chat_id))
        if not hinatachat:
            hinatachat = HinataChats(str(chat_id))
        SESSION.add(hinatachat)
        SESSION.commit()


def rem_hinata(chat_id):
    with INSERTION_LOCK:
        hinatachat = SESSION.query(HinataChats).get(str(chat_id))
        if hinatachat:
            SESSION.delete(hinatachat)
        SESSION.commit()
