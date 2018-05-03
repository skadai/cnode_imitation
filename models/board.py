import time
from models import Model, SQLMixin, SQLBase
from sqlalchemy import Column, String


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct


class BoardSQL(SQLBase, SQLMixin):
    __tablename__ = 'Board'
    title = Column(String(50), nullable=False, default='默认')


