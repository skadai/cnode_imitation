import hashlib
from sqlalchemy import Column, String
from models import Model, SQLMixin, SQLBase


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.image = form.get('image', "")
        self.signature = form.get('signature', "这家伙很懒，什么签名也没留下")

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @staticmethod
    def hashed_password(pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    def update(self, form):
        for k, v in form.items():
            setattr(self, k, v)
        self.save()


class UserSQL(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default=u"/images/3.jpg")
    signature = Column(String(200), nullable=False, default='nothing at all')

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    def get_signature(self):
        return self.signature

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        # pwd = form.get('password', '')

        if len(name) > 2 and not cls.exist(username=name):
            # 错误，只应该 commit 一次
            # u = User.new(**form)
            # u.password = u.salted_password(pwd)
            # User.session.add(u)
            # User.session.commit()
            u = cls.new(**form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=cls.salted_password(form['password']),
        )
        e = cls.exist(**query)
        if e:
            return cls.one(**query)
        else:
            return None
