from ..db_model.mysqldb_conn import conn_mysqldb
# from .Dinner import Dinner
import time

class DinnerOption:
    def __init__(self, menu_id, content):
        self.menu_id = menu_id
        self.content = content
        self.option_id = str(time.time()) + menu_id
    
    @staticmethod
    def getValidOptions(din_id):
        options = getDetails(din_id)

        db_conn = conn_mysqldb()
        cursor = db_conn.cursor()

        sql = """
                SELECT menu_id, menu_name, normal_price, extra_price
                FROM menus
                WHERE menu_id not in (
                    SELECT menu_id
                    FROM din_menu_map
                    WHERE dinner_id=%s
                );
                """
        
        cursor.execute(sql, din_id)
        data = cursor.fetchall()
        db_conn.close()

        extra = []
        for row in data:
            tmp = {
                'menuId': row[0],
                'menuName': row[1],
                'normalPrice': row[2],
                'extraPrice': row[3],
            }

            extra.append(tmp)
        
        return { 'options': options, 'extra': extra }

# avoid cuicular import
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