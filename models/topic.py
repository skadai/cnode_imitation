import time

from models.reply import Reply

from models import Model
from models.user import User


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
