from sqlalchemy import Column, String

from models import reset_database, SQLMixin, SQLBase
from models.user1 import User


class Test(SQLMixin, SQLBase):
    __tablename__ = 'Test'
    username = Column(String(20), nullable=False)


def main():
    reset_database()

    t = Test.new(
        username='test username'
    )
    # t.username
    # Test.usrename

    # User.new(
    #     username='gua',
    #     password='123',
    # )
    #
    # User.new(
    #     username='guagua',
    #     password='123',
    # )
    # print(User.exist(id=1))
    # print(User.exist(id=3))


if __name__ == '__main__':
    main()
