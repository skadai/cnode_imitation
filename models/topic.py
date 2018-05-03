import time
from sqlalchemy import Column, String, Integer

from models.reply import ReplySQL as Reply
from models.user import UserSQL as User
from models import Model, SQLMixin, SQLBase


class Topic(Model):
    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        # created time
        self.created_time = int(time.time())
        # updated time
        self.updated_time = self.created_time
        self.user_id = form.get('user_id', '')

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def relevant_users(self):
        users = {}
        for reply in self.replies():
            users[reply.user_id] = reply.updated_time
        return users

    @classmethod
    def user_participated(cls, user):
        topics = []

        for topic in cls.all():
            users = topic.relevant_users()
            if user.id in users:
                topic.updated_time = users[user.id]
                topics.append(topic)
        return topics


class TopicSQL(SQLBase, SQLMixin):
    __tablename__ = 'Topic'
    view = Column(Integer, nullable=False, default=0)
    title = Column(String(100), nullable=False)
    content = Column(String(3000), nullable=False, default='这个用户很懒，啥也没说')
    user_id = Column(Integer, nullable=False, default=0)
    board_id = Column(Integer, nullable=False, default=-1)

    @classmethod
    def get(cls, id):

        m = cls.exist(id=id)
        if m:
            m = cls.one(id=id)
            m.view += 1
            SQLMixin.session.add(m)
            SQLMixin.session.commit()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def relevant_users(self):
        users = {}
        for reply in self.replies():
            users[reply.user_id] = reply.updated_time
        return users

    @classmethod
    def user_participated(cls, user):
        topics = []
        for topic in cls.all():
            users = topic.relevant_users()
            if user.id in users:
                topic.updated_time = users[user.id]
                topics.append(topic)
        return topics
