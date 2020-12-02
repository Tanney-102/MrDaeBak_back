import hashlib
import bcrypt
from flask import Flask, jsonify, request
from ..db_model.mysqldb_conn import conn_mysqldb

class AccountManagenent:
    @staticmethod
    def findUserName(username):
        db_conn = conn_mysqldb()
        mds_db = db_conn.cursor()
        
        message = ''                                #상황에 따른 메시지
        check_dup = 'true'                          #중복확인 성공 여부

        username = username.strip()                 #좌우 공백 제거
        if not username:                                            #name 썼는지 확인
            check_dup = 'false'
            message = 'Need Name'

        else :
            sql = 'SELECT * from user_info where user_name=%s'      #닉네임 중복 확인
            cnt = mds_db.execute(sql, username)

            if cnt:                                                 #중복
                check_dup = 'false'
                message = 'Unavailable Name'

            else:                                                   #안중복
                message = 'available Name'
        
        db_conn.close()

        return [message] + [check_dup]                              #json으로 보낼 데이터 return


    @staticmethod
    def findUserId(userid):
        db_conn = conn_mysqldb()
        mds_db = db_conn.cursor()

        message = ''                                #상황에 따른 메시지
        check_dup = 'true'                          #중복확인 성공 여부

        id = userid.strip()                         #좌우 공백 제거          
        if not id:                                                  #id 썼는지 확인
            check_dup = 'false'
            message = 'Need Id'
        else:
            sql = 'SELECT * from user_info where user_id=%s'        #id 중복 확인
            cnt = mds_db.execute(sql, id)

            if cnt:                                                 #중복
                check_dup = 'false'
                message = 'Unavailable Id'

            else:                                                   #안중복
                message = 'available Id'

        db_conn.close()

        return [message] + [check_dup]                              #json으로 보낼 데이터 return


    @staticmethod
    def registerAccount(user_info):
        db_conn = conn_mysqldb()
        mds_db = db_conn.cursor()

        message = ''                                #상황에 따른 메시지
        success_signup = 'true'                     #회원가입 성공 여부
        
        username = user_info['user_name'].strip()       #좌우 공백 제거
        id = user_info['user_id'].strip()
        password = user_info['user_password'].strip()
                                                    
        if not username or not id or not password:      #안쓴거 있나 확인
            success_signup = 'false'
            message = 'Insert Error'

        if user_info['check_name_dup'] == 'false':      #닉네임 중복확인 여부
            success_signup = 'false'
            message = 'Check Name Duplicate'

        if user_info['check_id_dup'] == 'false':        #id 중복확인 여부
            success_signup = 'false'
            message = 'Check Id Duplicate'

        if success_signup == 'true':                    #데이터 문제 없음
            password = bcrypt.hashpw(user_info['user_password'].encode('utf-8'),bcrypt.gensalt())   #비밀번호 hash
            
            sql = """INSERT INTO user_info (user_name, user_id, password, class) VALUES (%s, %s, %s, 'member');"""   #db에 저장
            mds_db.execute(sql, (username, id, password))
            db_conn.commit() 

            message = 'Success signup'                  #회원가입 성공
        
        db_conn.close()

        return [message] + [success_signup]
