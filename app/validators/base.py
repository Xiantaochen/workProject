from wtforms import Form
from app.libs.error_code import ParameterException
from flask import request

class BaseForm(Form):
    def __init__(self, requset):
        data = requset.get_json(silent=True)
        args =request.args.to_dict()
        super(BaseForm,self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self