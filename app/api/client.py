from flask import request
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.model.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('token')

@api.route('/register',methods=['POST'])
def create_client():
    form = ClientForm(request).validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL : _register_user_by_emial
    }
    promise[form.type.data]()

    return Success

def _register_user_by_emial():
    form = UserEmailForm(request).validate_for_api()
    User.register_by_email(form.nickname.data,form.account.data,form.secret.data)