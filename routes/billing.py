from flask import Blueprint, request, jsonify
from utils.db import execute_query
from utils.notify import send_bill_email
from datetime import date
import json

billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/quota/<int:member_id>', methods=['GET'])
def get_quota(member_id):
    # Get card_id for this member
    member = execute_query(
        "SELECT card_id FROM family_members WHERE member_id = %s",
        (member_id,), fetch=True
    )
    if not member:
        return jsonify({'success': False, 'message': 'Member not found'}), 404

    card_id = member[0]['card_id']

    # Get family quota
    quota = execute_query(
        "SELECT * FROM family_quota WHERE card_id = %s",
        (card_id,), fetch=True
    )
    if not quota:
        return jsonify({'success': False, 'message': 'Family quota not found'}), 404

    q = quota[0]
    remaining = {
        'rice': round(q['rice'] - q['rice_used'], 2),
        'sugar': round(q['sugar'] - q['sugar_used'], 2),
        'oil': round(q['oil'] - q['oil_used'], 2)
    }
    return jsonify({'success': True, 'remaining_quota': remaining, 'card_id': card_id})


@billing_bp.route('/quota/full/<int:member_id>', methods=['GET'])
def get_full_quota(member_id):
    member = execute_query(
        "SELECT card_id FROM family_members WHERE member_id = %s",
        (member_id,), fetch=True
    )
    if not member:
        return jsonify({'success': False}), 404

    card_id = member[0]['card_id']

    quota = execute_query(
        "SELECT rice, sugar, oil FROM family_quota WHERE card_id = %s",
        (card_id,), fetch=True
    )
    if not quota:
        return jsonify({'success': False}), 404

    return jsonify({'success': True, 'quota': quota[0]})


@billing_bp.route('/bill', methods=['POST'])
def generate_bill():
    data = request.json
    member_id = data.get('member_id')
    items = data.get('items')

    # Get card_id for this member
    member = execute_query(
        "SELECT card_id FROM family_members WHERE member_id = %s",
        (member_id,), fetch=True
    )
    if not member:
        return jsonify({'success': False, 'message': 'Member not found'}), 404

    card_id = member[0]['card_id']

    # Get FAMILY quota (shared across all members)
    quota = execute_query(
        "SELECT * FROM family_quota WHERE card_id = %s",
        (card_id,), fetch=True
    )
    if not quota:
        return jsonify({'success': False, 'message': 'Family quota not found'}), 404

    q = quota[0]

    # Check each item against FAMILY remaining quota
    errors = []
    for item, qty in items.items():
        used_key = f"{item}_used"
        limit_key = item
        if used_key in q and limit_key in q:
            remaining = round(q[limit_key] - q[used_key], 2)
            if qty > remaining:
                errors.append(f"{item}: requested {qty} but only {remaining} remaining for this family")

    if errors:
        return jsonify({'success': False, 'message': 'Family quota exceeded', 'errors': errors}), 400

    # Deduct from FAMILY quota
    for item, qty in items.items():
        execute_query(
            f"UPDATE family_quota SET {item}_used = {item}_used + %s WHERE card_id = %s",
            (qty, card_id)
        )

    # Save transaction
    total_qty = round(sum(items.values()), 2)
    execute_query(
        "INSERT INTO transactions (member_id, items_purchased, total_quantity) VALUES (%s, %s, %s)",
        (member_id, json.dumps(items), total_qty)
    )

    # Get bill_id
    bill = execute_query(
        "SELECT bill_id FROM transactions WHERE member_id = %s ORDER BY date_time DESC LIMIT 1",
        (member_id,), fetch=True
    )

    bill_id = bill[0]['bill_id']

    # Send email notification
    notif_status = send_bill_email(member_id, bill_id, items, total_qty)

    # Update notification status
    execute_query(
        "UPDATE transactions SET notification_status = %s WHERE bill_id = %s",
        (notif_status, bill_id)
    )

    return jsonify({
        'success': True,
        'bill_id': bill_id,
        'member_id': member_id,
        'card_id': card_id,
        'items': items,
        'total_quantity': total_qty,
        'notification_status': notif_status,
        'message': 'Bill generated successfully'
    })