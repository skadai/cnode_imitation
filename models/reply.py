import time
from models import Model, SQLMixin, SQLBase
from models.user import UserSQL as User
from models.mail import MailSQL as Mail
from sqlalchemy import Column, String, Integer


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.created_time = int(time.time())
        self.updated_time = self.created_time

        self.content = form.get('content', '')
        self.topic_id = int(form.get('topic_id', -1))
        self.user_id = int(form.get('user_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u


class ReplySQL(SQLBase, SQLMixin):
    __tablename__ = 'Reply'
    content = Column(String(200), nullable=False, default='这个用户很懒，啥也没说')
    topic_id = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False, default=0)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def add_mail(self):
        receivers = []
        content = ''
        for tag in self.content.split(' '):
            if tag.startswith('@'):
                receivers.append(tag[1:])
            else:
                content += tag

        for r in receivers:
            if User.exist(username=r):
                receiver = User.one(username=r)
                form = dict(
                    title='你被{} @ 了'.format(self.user().username),
                    content='{} 点击<a href="/topic/{}">链接</a>查看'.format(content, self.topic_id),
                    sender_id=self.user_id,
                    receiver_id=receiver.id
                )
                Mail.new(**form)
