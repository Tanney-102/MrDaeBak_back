from ..db_model.mysqldb_conn import conn_mysqldb
from .Dinner import Dinner
from ..stock_management.StockManagement import StockManagement as Stock
import math

class SoldOutMonitor:
    def __init__(self):
        self.dinnerState = []

        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        cursor.execute('SELECT * FROM dinner')
        dinnerInfo = cursor.fetchall()

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
                
                if curSize > curStock:
                    tmpState['orderable'] = 'false'
            
            self.dinnerState.append(tmpState)
