from sqlalchemy import Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import NotFound, AuthFailed
from app.model.base import Base, db

class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    auth =Column(SmallInteger, default=1)
    nickname = Column(String(24), nullable=True)
    _password = Column('password',String(123))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', "email", "nickname"]

    def keys(self):
        return self.fields

    def hiden(self, **keys):
        [self.fields.remove(key) for key in keys]

    def append(self, **keys):
        [self.fields.append(key) for key in keys]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        if not self._password:
            return False
        return check_password_hash(self._password, password)

    @classmethod
    def register_by_email(nickname, account , secret):
        with db.auto_commit():
            user = User
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @classmethod
    def verify(email, passord):
        user= User.query.filter_by(email = email).firt_or_404()
        if not user.check_password(passord):
            raise AuthFailed()
        scope = 'SuperScope' if user.auth ==2 else 'UserScope'
        return {'uid':user.id , 'scope':scope}


