from flask import Blueprint, jsonify, request
from ..stock_management.StockManagement import StockManagement as SM

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock')

@stock_controller.route('/read', methods=['get'])
def getStockInfo():
    return jsonify(SM.getStock())

@stock_controller.route('/update', methods=['post'])
def setStockInfo():
    s = SM.setStock(request.get_json())
    if s:
        return jsonify({ 'result' : 'success' })