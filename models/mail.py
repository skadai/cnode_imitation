import time
from models import Model


class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.sender_id = form.get('sender_id', '')
        self.receiver_id = form.get('receiver_id', '')

        self.ct = int(time.time())
        self.ut = self.ct
