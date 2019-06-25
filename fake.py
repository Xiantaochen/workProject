from app import create_app
from app.model.base import db
from app.model.user import User

app = create_app()
with app.app_context():
    user = User()
    user.nickname = 'super'
    user.password = '123456'
    user.email = '999@qq.com'
    user.auth = 2
    db.session.add(user)