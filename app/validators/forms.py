from wtforms import StringField, IntegerField
from wtforms.validators import Regexp,  DataRequired, ValidationError,Email,length

from app.libs.enums import ClientTypeEnum
from app.model.user import User
from app.validators.base import BaseForm

class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(),length(min=8, max=16)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except Exception as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='Validate Email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_*$&#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(),length(min=2, max=32)])
    def validate_account(self, value):
        if User.query.filter_by(email = value.data).first():
            raise ValidationError(message='该账号已经存在')

class TokenForm(BaseForm):
    Token = StringField(validators=[DataRequired()])