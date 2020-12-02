import time
import datetime
import math
import pymysql
from .Dinner import Dinner
from ..user_management.User import Member
from ..stock_management.StockManagement import StockManagement as Stock
from ..db_model.mysqldb_conn import conn_mysqldb

class Order:
    """
        주문 정보 저장하고 DB에 등록하는 클래스
        staticmethod인 getOrderInfo를 통해 당일 주문 정보를 가져온다.

        orderInfo = {
            userId: '',
            mealNum: 0,
            resTime: '',
            address: '',
            paymentInfo: '',
            dinnerInfo: {
                dinnerId: '',
                dinnerName: '',
                dinnerStyle: '',
                options : [],
            }
        }

        getOrderInfo의 반환값
        ret = {
            '17:00': [
                {
                    dinnerName: '',
                    dinnerStyle: '',
                    mealNum: 0,
                    userName: '',
                    address: '',
                    paymentInfo: '',
                    options: [
                        menuName: '',
                        detail: '',
                    ],
                }
            ],
            .....
        }
    """
    def __init__(self, orderInfo):
        self.orderId = ''
        self.mealNum = 0
        self.resTime = ''
        self.address = ''
        self.paymentInfo = ''
        self.dinnerInfo = None
        self.user = None
        self.details = []

        self.setOrderInfo(orderInfo)

    def setOrderInfo(self, orderInfo):
        self.orderId = str(time.time()) + orderInfo['userId']
        self.mealNum = orderInfo['mealNum']
        self.resTime = orderInfo['resTime']
        self.paymentInfo = orderInfo['paymentInfo']
        self.dinnerInfo = Dinner(orderInfo['dinnerInfo'], self.orderId)
        self.user = Member(orderInfo['userId'])
        self.address = orderInfo['address']

        tmpDetail = Dinner.getDetails(self.dinnerInfo.getInfo()['dinnerId'])
        for tmpD in tmpDetail:
            self.details.append({
                'menuId': tmpD['menuId'],
                'size': tmpD['size'],
                'measure': tmpD['measure'],
                'remove': False,
                'extra': False,
            })
        
        for op in self.dinnerInfo.getInfo()['option']:
            if op.getInfo()['content'] == 'remove':
                for t in self.details:
                    if t['menuId'] == op.getInfo()['menuId']:
                        t['remove'] = True
                        break
            elif op.getInfo()['content'].find('add') > -1:
                self.details.append({
                    'menuId': op.getInfo()['menuId'],
                    'size': 1,
                    'measure': '',
                    'remove': False,
                    'extra': False
                })
            elif op.getInfo()['content'].find('sizeup') > -1:
                for t in self.details:
                    if t['menuId'] == op.getInfo()['menuId']:
                        t['extra'] = True
                        break


    def registerOrder(self):
        curDate = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
        
        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        sql_order = """
                INSERT INTO order_list
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        
        sql_option = """
                INSERT INTO option_list
                VALUES (%s, %s, %s, %s);
                """

        try:
            cursor.execute(sql_order, (
                self.orderId,
                self.dinnerInfo.style,
                self.mealNum,
                curDate+' '+self.resTime,
                self.user.getId(),
                self.dinnerInfo.getInfo()['dinnerId'],
                self.user.getName(),
                self.dinnerInfo.getInfo()['dinnerName'],
                self.address,
                self.paymentInfo
            ))
        except pymysql.err.InternalError as e:
                code, msg = e.args
                print(code, msg)

        for op in self.dinnerInfo.getInfo()['option']:
            try:
                cursor.execute(sql_option, (
                    op.getInfo()['optionId'],
                    op.getInfo()['menuId'],
                    op.getInfo()['content'],
                    op.getInfo()['orderId'],
                ))
            except pymysql.err.InternalError as e:
                code, msg = e.args
                print(code, msg)

        db_conn.commit()
        db_conn.close()

        self.updateStock()
        self.user.setAddress(self.address);
        self.user.addOrderNum();
        self.user.setClass();
        
        return True

    def updateStock(self):
        newStocks = []

        for det in self.details:
            if det['remove']:
                continue
                
            size = det['size']
            if not det['extra']:
                if det['measure'] == 'pot':
                    size *= 5
                elif det['measure'] == 'bottle':
                    size *= 8
            else:
                if det['measure'] == 'pot':
                    size *= 10
                elif det['measure'] == 'bottle':
                    size *= 16
                elif det['measure'] == '':
                    size *= 1.5
                else:
                    size = math.ceil(size*1.5)

            stockSubt = 0
            if det['measure'] == 'pot' or det['measure'] == 'bottle':
                stockSubt = -size
            else:
                stockSubt = -size * self.mealNum

            newStocks.append({
                'menu_id': det['menuId'],
                'stock': stockSubt,
            })
        
        Stock.setStock(newStocks)

    @staticmethod
    def getOrderInfo():
        curDate = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
        orderTable = {
            '17:00': [],
            '18:00': [],
            '19:00': [],
            '20:00': [],
            '21:00': [],
        }

        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        sql_order = """
                SELECT dinner_name, style, meal_num, user_name, address, payment_info, order_id, reservation
                FROM order_list
                WHERE reservation like %s
                """

        sql_option = """
                SELECT me.menu_name, op.detail
                FROM option_list op, menus me
                WHERE op.order_id=%s and op.menu_id=me.menu_id
                """
        
        
        cursor.execute(sql_order, curDate+'%%')
        orderInfo = cursor.fetchall()

        for od in orderInfo:
            _orderId = od[6]
            _resTime = od[7].split(sep=' ')[1]

            tmp = {
                'dinnerName': od[0],
                'dinnerStyle': od[1],
                'mealNum': od[2],
                'userName': od[3],
                'address': od[4],
                'paymentInfo': od[5],
                'resTime': _resTime,
                'options': [],
            }

            cursor.execute(sql_option, _orderId)
            optionInfo = cursor.fetchall()

            for op in optionInfo:
                tmpOption = {
                    'menuName': op[0],
                    'detail': op[1]
                }

                tmp['options'].append(tmpOption)
            
            orderTable[_resTime].append(tmp)
        
        db_conn.close()

        return orderTable


