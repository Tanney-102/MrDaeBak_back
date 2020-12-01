from flask import jsonify, request, Blueprint
from pakages.order_management.SoldOutMonitor import SoldOutMonitor

order_controller = Blueprint('order_controller', __name__)

@order_controller.route('/orderstate', methods=['GET'])
def getOrderState():
    return jsonify(SoldOutMonitor().dinnerState)