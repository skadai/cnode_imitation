from sqlalchemy import Column, String

from models import reset_database, SQLMixin, SQLBase
from models.user import UserSQL as User
from models.topic import TopicSQL as Topic
from models.reply import ReplySQL as Reply
from models.board import BoardSQL as Board
from models.mail import MailSQL as Mail

from fake import test


class Test(SQLMixin, SQLBase):
    __tablename__ = 'Test'
    username = Column(String(20), nullable=False)


def main():
    reset_database()
    test()


if __name__ == '__main__':
    main()
