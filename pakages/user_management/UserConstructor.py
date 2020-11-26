import jwt
import bcrypt
from flask import jsonify
from .User import Member, Manager

class UserConstructor:
    @staticmethod
    def loginAsMember(login_info):           #member 로그인
        id = login_info['user_id']                             #입력된 정보 분류 
        pw = login_info['user_password']
        login_type = login_info['login_type']

        user = Member(id)    #user객체 생성
        message = 'login As Member'         
        success_login = 'true'
        access_token = ''

        if user.getId() != '':
            hashedPw = user.getPw()

            is_pw_correct = bcrypt.checkpw(pw.encode('UTF-8'), hashedPw.encode('UTF-8'))     #비밀번호 비교 
            is_class_correct = (login_type == 'member')

            if is_pw_correct:
                if is_class_correct:
                    payload = {
                        'user_id' : id
                    }
                    access_token = jwt.encode(payload, 'asdasdasd', 'HS256')
                    return message, success_login, access_token.decode('utf8'), user
                else:
                    message = 'invalid class'
                    success_login = 'false'
            else:
                message = 'invalid pw'
                success_login = 'false'
        else:
            message = 'invalid id'
            success_login = 'false'
        
        return message, success_login, access_token, user


    @staticmethod
    def loginAsManager(login_info):          #manager 로그인
        id = login_info['user_id']                             #입력된 정보 분류 
        pw = login_info['user_password']
        login_type = login_info['login_type']

        user = Manager(id)    #user객체 생성
        message = 'login As Manager'         
        success_login = 'true'
        access_token = ''

        if user.getId() != '':
            hashedPw = user.getPw()

            is_pw_correct = bcrypt.checkpw(pw.encode('UTF-8'), hashedPw.encode('UTF-8'))     #비밀번호 비교 
            is_class_correct = (login_type == 'manager')

            if is_pw_correct:
                if is_class_correct:
                    payload = {
                        'user_id' : id
                    }
                    access_token = jwt.encode(payload, 'asdasdasd', 'HS256')
                    return message, success_login, access_token.decode('utf8'), user
                else:
                    message = 'invalid class'
                    success_login = 'false'
            else:
                message = 'invalid pw'
                success_login = 'false'
        else:
            message = 'invalid id'
            success_login = 'false'
        
        return message, success_login, access_token, user