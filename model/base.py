from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import SmallInteger, Column, Integer
from datetime import datetime
from contextlib import contextmanager
from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if "status" not in kwargs:
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv= self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        def first_or_404(self):
            rv = self.first()
            if not rv:
                raise NotFound()
            return rv

db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger,default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())


    def __getitem__(self, item):
        return getattr(self.item)

    def set_attrs(self, attr_dict):
        for key , value in attr_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self,key, value)

    def delete(self):
        self.status = 0

    @property
    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

