from abc import *
from random import randint
from ..db_model.mysqldb_conn import conn_mysqldb

class User(metaclass=ABCMeta):
    id = ''
    name = ''
    hashedPw = ''
    classification = ''
    address = ''

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getPw(self):
        return self.hashedPw

    def getClass(self):
        return self.classification

    def getAddress(self):
        return self.address
    
    def setAddress(self, new_address):
        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        sql = """
                UPDATE user_info 
                SET address=%s 
                WHERE user_id=%s
                """

        db_cursor.execute(sql, (new_address, self.id))
        db_conn.commit()
        db_conn.close()

    @staticmethod
    def getBasicInfo(user_id):
        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        sql = """
                SELECT user_name, class, address
                FROM user_info
                WHERE user_id=%s
                """

        db_cursor.execute(sql, user_id)
        info = db_cursor.fetchone()
        user_name, classification, address = info
        
        db_conn.close()
        
        return user_name, classification, address


class Member(User):
    def __init__(self, user_id):
        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()
        
        sql = """
                SELECT user_name, password, address, ordered_num, class
                FROM user_info
                WHERE user_id=%s
                """
        
        row_cnt = db_cursor.execute(sql, user_id)

        if row_cnt > 0:
            info = db_cursor.fetchone()

            self.id = user_id
            self.name = info[0]
            self.hashedPw = info[1]
            self.address = info[2]
            self.ordered_num = info[3]
            self.ordered_num_added = False
            self.classification = info[4]

        db_conn.close()
    
    def getOrderNum(self):
        return self.ordered_num

    def addOrderNum(self):
        self.ordered_num += 1
        self.ordered_num_added = True

        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        sql = """
                UPDATE user_info 
                SET ordered_num=%s
                WHERE user_id=%s
                """

        db_cursor.execute(sql, (self.ordered_num, self.id))
        db_conn.commit()
        db_conn.close()
    
    def setClass(self):
        '''
        디너 주문 완료시 호출하며 ordered_num이 15회가 되는 순간 classification이 vip로 바뀌도록 한다.
        반드시 addOrderNum 메서드가 먼저 호출 되어야 한다.
        '''

        if not self.ordered_num_added:
            raise Exception('ooder_num has not been added.')

        if self.classification == 'member' and self.ordered_num >= 15:
            self.classification = 'vip'

            db_conn = conn_mysqldb()
            db_cursor = db_conn.cursor()

            sql = """
                    UPDATE user_info 
                    SET class=%s
                    WHERE user_id=%s
                    """

            db_cursor.execute(sql, ('vip', self.id))
            db_conn.commit()
            db_conn.close()


class Manager(User):
    def __init__(self, user_id):
        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()
        
        sql = """
                SELECT user_name, password
                FROM user_info
                WHERE user_id=%s
                """
        
        row_cnt = db_cursor.execute(sql, user_id)

        if row_cnt > 0:
            info = db_cursor.fetchone()

            self.id = user_id
            self.name = info[0]
            self.hashedPw = info[1]
            self.classification = 'manager'

        db_conn.close()