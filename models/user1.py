import hashlib

from sqlalchemy import Column, String, ForeignKey

from models import Model, SQLMixin, SQLBase


class User(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/3.jpg')

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and not User.exist(username=name):
            # 错误，只应该 commit 一次
            # u = User.new(**form)
            # u.password = u.salted_password(pwd)
            # User.session.add(u)
            # User.session.commit()
            u = User.new(**form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        e = User.exist(**query)
        if e:
            return User.one(**query)
        else:
            return None
