from flask import Blueprint, request, jsonify
from utils.db import execute_query

members_bp = Blueprint('members', __name__)

@members_bp.route('/family/<card_id>', methods=['GET'])
def get_family(card_id):
    members = execute_query(
        "SELECT member_id, name, age, gender, face_image_path FROM family_members WHERE card_id = %s",
        (card_id,),
        fetch=True
    )

    if not members:
        return jsonify({'success': False, 'message': 'No family found for this card'}), 404

    return jsonify({'success': True, 'members': members})