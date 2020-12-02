from flask import Blueprint, jsonify
from ..db_model.mysqldb_conn import conn_mysqldb

test_module = Blueprint('test_module', __name__)

@test_module.route('/db_test')
def db_test():
    db = conn_mysqldb()
    db_cursor = db.cursor()
    sql = "select * from user_info"
    db_cursor.execute(sql)
    user_row = db_cursor.fetchone()

    user = {
        'user_id' : user_row[0],
        'user_name' : user_row[1],
        'user_pw' : user_row[2],
        'address' : user_row[3],
        'ordered' : user_row[4],
        'class' : user_row[5]
    }

    return jsonify(user)

@test_module.route('/get_m_test/<id>')
def get_m_test(id):
    return '<h1>%s</h1>' % id