from flask import jsonify, request, Blueprint
from ..order_management.SoldOutMonitor import SoldOutMonitor
from ..order_management.DinnerOption import DinnerOption
from ..order_management.Order import Order


order_controller = Blueprint('order_controller', __name__)

@order_controller.route('/orderstate', methods=['GET'])
def getOrderState():
    return jsonify(SoldOutMonitor().getdinnerState())

@order_controller.route('/options', methods=['GET'])
def getOptions():
    dinnerId = request.args.to_dict()['dinnerId']
    return jsonify(DinnerOption.getValidOptions(dinnerId))

@order_controller.route('/order', methods=['POST'])
def createOrder():
    Order(request.get_json()).registerOrder()
    return jsonify({ 'success': 'success'})

@order_controller.route('/reservation', methods=['GET'])
def getReservationInfo():
    return jsonify(Order.getOrderInfo())