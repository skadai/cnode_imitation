from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from models.user import UserSQL as User
from models.topic import TopicSQL as Topic
from models.reply import ReplySQL as Reply
from models.board import BoardSQL as Board
from models.mail import MailSQL as Mail


def users(count=5):
    fake = Faker()
    i = 0
    while i < count:
        u = User.new(username=fake.user_name(),
                 password='123')
        User.session.add(u)
        try:
            User.session.commit()
            i += 1
        except IntegrityError:
            User.session.rollback()


def boards(count=5):
    fake = Faker()
    i = 0
    while i < count:
        u = Board.new(title=fake.text(10))
        Board.session.add(u)
        try:
            Board.session.commit()
            i += 1
        except IntegrityError:
            Board.session.rollback()


def topics(count=50):
    fake = Faker()
    user_count = User.query.count()
    board_count = Board.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count-1)).first()
        b = Board.query.offset(randint(0, board_count-1)).first()
        p = Topic.new(views=randint(0,1000),
                  title=fake.text(10),
                  content=fake.text(),
                  board_id=b.id,
                  user_id=u.id)
        Topic.session.add(p)
    Topic.session.commit()


def replies(count=100):
    fake = Faker()
    topic_count = Topic.query.count()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count-1)).first()
        t = Topic.query.offset(randint(0, topic_count-1)).first()
        p = Reply.new(
                  content= fake.text(),
                  topic_id = t.id,
                  user_id=u.id)
        Reply.session.add(p)
    Reply.session.commit()


def mails(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        p = Mail.new(
                  title= fake.text(10),
                  content = fake.text(100),
                  sender_id = randint(0, user_count-1),
                  receiver_id= randint(0, user_count-1))
        Mail.session.add(p)
    Mail.session.commit()


def test():
    # users()
    # boards()
    # topics()
    # replies()
    mails()

if __name__ == '__main__':
    test()