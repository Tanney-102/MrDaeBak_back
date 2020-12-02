from flask import Flask, jsonify
from flask_cors import CORS
from packages.db_model.mysqldb_conn import conn_mysqldb
from packages.router.test_module import test_module
from packages.router.SignupController import signup_controller
from packages.router.StockController import stock_controller
from packages.router.LoginController import login_controller
from packages.router.OrderController import order_controller

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "1111"

app.register_blueprint(test_module)
app.register_blueprint(signup_controller)
app.register_blueprint(stock_controller)
app.register_blueprint(login_controller)
app.register_blueprint(order_controller)

@app.route('/')
def index() :
    return '<h1>Mr DaeBak API Server!</h1>'


if __name__ == '__main__':
    app.run(debug=True)