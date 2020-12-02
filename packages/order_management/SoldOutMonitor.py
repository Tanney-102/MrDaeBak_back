from ..db_model.mysqldb_conn import conn_mysqldb
from .Dinner import Dinner
from ..stock_management.StockManagement import StockManagement as Stock
import math
import datetime

class SoldOutMonitor:
    """
        getDinnerState  
            -> 각 디너에 포함되는 메뉴의 재고를 확인하고 주문 가능 여부와 기본 정보를 반환
            -> 모든 재고의 품절여부는 size up한 양의 4인분을 기준으로 한다.

        getOrderedNum
            -> 각 시간대 별 주문 수 반환
    """
    def __init__(self):
        pass

    def getDinnerState(self):
        dinnerState = []
        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        cursor.execute('SELECT * FROM dinner')
        dinnerInfo = cursor.fetchall()
        print(dinnerInfo)

        for din_info in dinnerInfo:
            tmpState = {
                'dinnerId': din_info[0],
                'dinnerName': din_info[1],
                'orderable': 'true',
                'price': din_info[2],
                'special': 'false',
                'details': [],
            }

            if din_info[3]:
                tmpState['special'] = 'true'
            
            detailInfo = Dinner.getDetails(tmpState['dinnerId'])
            for d in detailInfo:
                tmp = {
                    'menuId': d['menuId'],
                    'size': int(d['size']),
                    'measure': d['measure']
                }
                tmpState['details'].append(tmp)

                curStock = Stock.getStock(d['menuId'])[0]['stock']
                curSize = d['size']

                if d['measure'] == 'pot':
                    curSize = math.ceil(curSize*1.5) * 5
                elif d['measure'] == 'bottle':
                    curSize = math.ceil(curSize*1.5) * 8
                elif d['measure'] == 'cup' or d['measure'] == 'glass' or d['measure'] == 'piece':
                    curSize = math.ceil(curSize*1.5)
                else:
                    curSize *= 1.5

                curSize*=4
                
                if curSize > curStock:
                    tmpState['orderable'] = 'false'
            
            dinnerState.append(tmpState)

        return dinnerState

    def getOrderedNum(self):
        orderedNum = {
            '17:00': 0,
            '18:00': 0,
            '19:00': 0,
            '20:00': 0,
            '21:00': 0,
        }

        curDate = datetime.datetime.now().strftime('%Y-%m-%d')
        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        sql = """
                SELECT reservation
                FROM order_list
                WHERE reservation like %s
                """

        cursor.execute(sql, curDate+'%%')
        orders = cursor.fetchall()
        print(curDate)
        print(orders)

        for od in orders:
            orderedNum[od[0].split(sep=' ')[1]] += 1

        return orderedNum


