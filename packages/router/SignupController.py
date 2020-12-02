from ..user_management import AccountManagenent as AM
import hashlib
import bcrypt
import json
from flask import Flask, jsonify, request, Blueprint

signup_controller = Blueprint('signup_controller', __name__)

@signup_controller.route('/signin_db', methods=['POST'])
def signup():
    data = request.form

    if request.method == 'POST':
        message, success_signup = AM.AccountManagenent.registerAccount(data)               
    
    return jsonify({'Success':success_signup, 'Message':message})

@signup_controller.route('/duplicate_name', methods=['POST'])
def isAvailableName():
    data = request.get_json()
    
    if request.method == 'POST':                    #AccountManagenent 호출
        message, check_dup = AM.AccountManagenent.findUserName(data['user_name'])
    
    return jsonify({'check_name_dup':check_dup, 'Message':message})


@signup_controller.route('/duplicate_id', methods=['POST'])
def isAvailableId():
    data = request.get_json()

    if request.method == 'POST':                    #AccountManagenent 호출      
        message, check_dup = AM.AccountManagenent.findUserId(data['user_id'])
        # print(AM.AccountManagenent.findUserId(data['user_id'], mds_db))
    
    return jsonify({'check_id_dup':check_dup, 'Message':message})
    
