from ..db_model.mysqldb_conn import conn_mysqldb
from ..user_management import UserConstructor as UC
from ..user_management.User import User
from flask import jsonify, request, Blueprint, Response
import jwt

login_controller = Blueprint('login_controller', __name__)

@login_controller.route('/login', methods=['GET', 'POST'])
def login():                    
    if request.method == 'GET':
        access_token = request.headers.get('Authorization')

        if access_token is not None:
            try:
                payload = jwt.decode(access_token, 'asdasdasd', 'HS256')
            except jwt.InvalidTokenError:
                payload = None
            
            if payload is None:
                return Response(status=401)
            
            user_id = payload['user_id']
            user_name, classification, address = User.getBasicInfo(user_id)

            return jsonify({
                'logged_in' : 'true',
                'user_id' : user_id,
                'user_name' : user_name,
                'address': address,
                'classification' : classification,
            })
        return jsonify({
            'logged_in' : 'false',
            'user_id' : '',
            'user_name': '',
            'address': '',
            'classification' : '',
        })
    elif request.method == 'POST':
        login_info = request.form

        if login_info['login_type'] == 'member':            
            message, success_login, access_token, user = UC.UserConstructor.loginAsMember(login_info)
        elif login_info['login_type'] == 'manager':        
            message, success_login, access_token, user = UC.UserConstructor.loginAsManager(login_info)

        return jsonify({
            'message':message, 
            'success':success_login, 
            'user_id':user.getId(),
            'user_name':user.getName(),
            'classification':user.getClass(), 
            'access_token':access_token
            })

@login_controller.route('/logout')
def logout():
    #아직 안됨
    return jsonify({'Success':'true'})