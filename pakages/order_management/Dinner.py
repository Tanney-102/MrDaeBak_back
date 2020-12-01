from ..db_model.mysqldb_conn import conn_mysqldb
from .DinnerOption import DinnerOption

class Dinner:
    def __init__(self, din_info):
        self.din_id = din_info.dinnerId
        self.name = din_info.dinnerName
        self.style = din_info.dinnerStyle
        self.options = []

        addOptions(din_info)
        

    def addOptions(self, info):
        for op in info.option:
            self.options.append(DinnerOption(op.menuId, op.detail))

    def getInfo(self):
        return {
            'dinnerId': self.din_id,
            'dinnerName': self.name,
            'dinnerStyle': self.style,
            'option': self.options
        }

    @staticmethod
    def getDetails(dinnerId):
        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        sql = """
                SELECT dmm.dinner_id, dmm.menu_id, me.menu_name, dmm.size, dmm.measure, me.normal_price, me.extra_price
                FROM din_menu_map dmm, menus me
                WHERE dmm.dinner_id=%s and dmm.menu_id=me.menu_id;
                """
        
        cursor.execute(sql, dinnerId)
        data = cursor.fetchall()
        db_conn.close()

        details = []
        for row in data:
            measure = ''
            if row[4] is not None:
                measure = row[4]
                
            tmp = {
                'menuId': row[1],
                'menuName': row[2],
                'size': row[3],
                'measure': measure,
                'normalPrice': row[5],
                'extraPrice': row[6]
            }

            details.append(tmp)
        
        return details