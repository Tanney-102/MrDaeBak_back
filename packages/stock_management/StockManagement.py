from ..db_model.mysqldb_conn import conn_mysqldb
import pymysql

class StockManagement:
    @staticmethod
    def getStock(id=None):
        """
            id(menu_id) 값을 받지 않으면 전체 행을 반환
            id가 있을 경우 해당하는 값만 반환

            반환 형태
            [
                {
                    menu_id: "..",
                    menu_name: "..",
                    stock: 0,
                    note: "..",
                }, {
                    ...
                }
            ]
        """
        db = conn_mysqldb()
        db_cursor = db.cursor()

        if id is None:
            sql = """
                    SELECT menu_id, menu_name, stock, note
                    FROM menus;
                    """
            db_cursor.execute(sql)
        else:
            sql = """
                    SELECT menu_id, menu_name, stock, note
                    FROM menus
                    WHERE menu_id=%s
                    """
            db_cursor.execute(sql, id)
        

        datas = []
        for _ in range(db_cursor.rowcount):
            menu_id, menu_name, stock, note = db_cursor.fetchone()
            datas.append({
                'menu_id' : menu_id,
                'menu_name': menu_name,
                'stock' : stock,
                'note' : note,
            })

        db.close()
        
        return datas

    @staticmethod
    def setStock(data: list[dict[str, str]]): 
        """
        인수 형태
            [
                {
                    menu_id: "..",
                    menu_name: "..",
                    stock: 0,
                    note: "..",
                }, {
                    ...
                }
            ]

            또는

            [
                {
                    menu_id: "..",
                    stock: 0,
                }, {
                    ...
                }
            ]

        stock이 음수일 경우 기존 stock에서 입력값만큼 빼서 저장
        """
        if data is None:
            return True

        db = conn_mysqldb()
        db_cursor = db.cursor()

        sql1 = """
                UPDATE menus
                SET menu_name=%s, stock=%s, note=%s
                WHERE menu_id=%s
                """

        sql2 = """
                UPDATE menus
                SET stock=%s
                WHERE menu_id=%s
                """

        for d in data:
            if int(d['stock']) < 0:
                db_cursor.execute('SELECT stock From menus WHERE menu_id=%s', d['menu_id'])
                d['stock'] = db_cursor.fetchone()[0] + d['stock']
                if d['stock'] < 0:
                    d['stock'] = 0

            if 'menu_name' in d:
                try:
                    db_cursor.execute(sql1, (d['menu_name'], str(d['stock']), d['note'], d['menu_id']))
                except pymysql.err.InternalError as e:
                    code, msg = e.args
                    print(code, msg)
            else:
                try:
                    db_cursor.execute(sql2, (str(d['stock']), d['menu_id']))
                except pymysql.err.InternalError as e:
                    code, msg = e.args
                    print(code, msg)

        db.commit() 
        db.close()

        return True