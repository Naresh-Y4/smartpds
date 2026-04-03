from flask import Blueprint, request, jsonify
from utils.db import execute_query
from utils.face_utils import capture_and_verify

face_bp = Blueprint('face', __name__)

@face_bp.route('/verify/<int:member_id>', methods=['POST'])
def verify_face(member_id):
    result = execute_query(
        "SELECT face_image_path FROM family_members WHERE member_id = %s",
        (member_id,),
        fetch=True
    )

    if not result or not result[0]['face_image_path']:
        return jsonify({'success': False, 'message': 'No stored face image for this member'}), 404

    image_path = result[0]['face_image_path']
    matched, message = capture_and_verify(image_path)

    return jsonify({'success': matched, 'message': message})