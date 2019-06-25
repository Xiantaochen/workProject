from flask import request, current_app, jsonify
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.validators.forms import TokenForm,ClientForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.model.user import User

api = Redprint('token')

@api.route('', methods=["POST"])
def get_token():
    form = ClientForm(request).validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    indentity = promise[form.type.data](
        form.account.data,
        form.secret.data
    )
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generator_auth_token(indentity['uid'],
                                 form.type.data,
                                 indentity["scope"],
                                 expiration=expiration)
    t= {
        'token':token.decode('utf-8')
    }
    return jsonify(token),201

@api.route('/secret', methods=['POST'])
def get_token_info():
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.load(form.token.data, return_header = True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
         raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)

def generator_auth_token(uid,ac_type,scope=None,expiration  = 7200):
    """生成令牌"""
    s = Serializer(current_app.config["SECRET_KEY"],expiration =expiration)
    return s.dumps({
       "uid" : uid,
        'type':ac_type,
        'scope':scope
    })