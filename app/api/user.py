from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.token_auth import auth
from flask import jsonify, g
from app.model.base import db

from app.model.user import User

api = Redprint('user')

@api.route('/<int:uid>',methods =["GET"])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id= uid).first_or_404()
    return jsonify(user)

@api.route('',methods=["GET"])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

@api.route('/<int:uid>', methods = ["DELETE"])
@auth.login_required
def super_delete_user(uid):
    with db.auto_commit():
        user   = User.query.filter_by(id = uid).first_or_404()
        user.delete()
    return DeleteSuccess()

@api.route('', methods=["DELETE"])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()

