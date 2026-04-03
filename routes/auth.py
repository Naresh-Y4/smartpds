from flask import Blueprint, request, jsonify, session
from utils.db import execute_query

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    shop_name = data.get('shop_name')
    password = data.get('password')

    result = execute_query(
        "SELECT * FROM shops WHERE shop_name = %s AND password = %s",
        (shop_name, password),
        fetch=True
    )

    if result:
        session['shop_id'] = result[0]['shop_id']
        session['shop_name'] = result[0]['shop_name']
        return jsonify({'success': True, 'shop': result[0]['shop_name']})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})