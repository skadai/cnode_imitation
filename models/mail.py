import time
from models import Model, SQLMixin, SQLBase
from sqlalchemy import Column, String, Integer
from models.user import UserSQL as User

class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.sender_id = form.get('sender_id', '')
        self.receiver_id = form.get('receiver_id', '')

        self.ct = int(time.time())
        self.ut = self.ct


class MailSQL(SQLBase, SQLMixin):
    __tablename__ = 'Mail'

    title = Column(String(50), nullable=False, default='这个用户很懒，啥也没说')
    content = Column(String(200), nullable=False, default='这个用户很懒，啥也没说')
    sender_id = Column(Integer, nullable=False, default=0)
    receiver_id = Column(Integer, nullable=False, default=0)

    def sender(self):
        if User.exist(id=self.sender_id):
            u = User.one(id=self.sender_id)
            return u.username
        return 'Anoymous'

    def receiver(self):
        if User.exist(id=self.receiver_id):
            u = User.one(id=self.receiver_id)
            return u.username
        return 'Anoymous'

