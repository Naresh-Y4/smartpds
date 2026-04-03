from flask import Blueprint, jsonify
from utils.qr_scanner import scan_qr_from_webcam
from utils.db import execute_query

qr_bp = Blueprint('qr', __name__)

@qr_bp.route('/scan', methods=['GET'])
def scan_qr():
    card_id = scan_qr_from_webcam()

    if not card_id:
        return jsonify({'success': False, 'message': 'No QR code detected'}), 400

    # Fetch family members for this card
    members = execute_query(
        "SELECT member_id, name, age, gender, face_image_path FROM family_members WHERE card_id = %s",
        (card_id,),
        fetch=True
    )

    if not members:
        return jsonify({'success': False, 'message': 'No family found for this card'}), 404

    return jsonify({
        'success': True,
        'card_id': card_id,
        'members': members
    })