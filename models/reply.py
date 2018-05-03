import time
from models import Model
from models.user import User


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

