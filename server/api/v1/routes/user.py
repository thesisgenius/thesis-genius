# api/v1/routes/user.py
from flask import Blueprint

user_bp_v1 = Blueprint('user_v1', __name__)

@user_bp_v1.route('/user', methods=['GET'])
def get_user():
    return {"message": "v1 user endpoint"}
