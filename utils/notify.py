import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from utils.db import execute_query
import json

def send_bill_email(member_id, bill_id, items, total_qty):
    """
    Fetch member email from DB.
    If email exists, send bill notification.
    Returns 'Sent', 'No Email', or 'Failed'
    """
    # Fetch member details
    member = execute_query(
        "SELECT name, email, phone_number FROM family_members WHERE member_id = %s",
        (member_id,),
        fetch=True
    )

    if not member:
        return 'Failed'

    member = member[0]
    email = member.get('email')

    if not email:
        print(f"No email for member {member_id} — skipping notification")
        return 'No Email'

    # Build email
    subject = f"[Smart PDS] Ration Bill #{bill_id} — Transaction Confirmation"
    body = build_email_body(member['name'], bill_id, items, total_qty)

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"Smart PDS System <{EMAIL_SENDER}>"
        msg['To'] = email

        # Plain text version
        text_part = MIMEText(build_plain_text(member['name'], bill_id, items, total_qty), 'plain')
        # HTML version
        html_part = MIMEText(body, 'html')

        msg.attach(text_part)
        msg.attach(html_part)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, msg.as_string())

        print(f"Email sent to {email} for bill #{bill_id}")
        return 'Sent'

    except Exception as e:
        print(f"Email failed: {e}")
        return 'Failed'


def build_plain_text(name, bill_id, items, total_qty):
    lines = [
        f"Dear {name},",
        f"",
        f"Your ration bill has been generated successfully.",
        f"Bill ID   : #{bill_id}",
        f"Items     : {', '.join([f'{k}: {v}kg' for k, v in items.items()])}",
        f"Total Qty : {total_qty} kg",
        f"",
        f"Thank you.",
        f"Smart PDS System — Government of Tamil Nadu"
    ]
    return "\n".join(lines)


def build_email_body(name, bill_id, items, total_qty):
    item_rows = ""
    item_names = {'rice': '🌾 Rice', 'sugar': '🍬 Sugar', 'oil': '🫙 Oil'}
    units = {'rice': 'kg', 'sugar': 'kg', 'oil': 'L'}

    for item, qty in items.items():
        item_rows += f"""
        <tr>
            <td style="padding:10px 14px;border-bottom:1px solid #f0f0f0;">{item_names.get(item, item)}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #f0f0f0;font-weight:600;color:#1a237e;">{qty} {units.get(item,'kg')}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #f0f0f0;">
                <span style="background:#e8f5e9;border:1px solid #a5d6a7;color:#2e7d32;font-size:11px;padding:2px 8px;border-radius:2px;">✓ Issued</span>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f0f2f5;font-family:Arial,sans-serif;">

      <div style="max-width:580px;margin:30px auto;background:#fff;border-radius:4px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">

        <!-- Header -->
        <div style="background:#1a237e;padding:0;">
          <div style="height:4px;background:linear-gradient(90deg,#ff6b00 33%,#fff 33%,#fff 66%,#138808 66%);"></div>
          <div style="padding:20px 28px;display:flex;align-items:center;">
            <div>
              <div style="font-size:18px;font-weight:700;color:#fff;">⚡ Smart PDS System</div>
              <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:2px;">Government of Tamil Nadu · பொது விநியோக முறை</div>
            </div>
          </div>
        </div>

        <!-- Success bar -->
        <div style="background:#138808;padding:14px 28px;display:flex;align-items:center;gap:12px;">
          <span style="font-size:24px;">✅</span>
          <div>
            <div style="font-size:15px;font-weight:600;color:#fff;">Bill Generated Successfully</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.8);">Your ration has been issued. Keep this for reference.</div>
          </div>
        </div>

        <!-- Body -->
        <div style="padding:24px 28px;">

          <p style="font-size:14px;color:#333;margin-bottom:20px;">Dear <strong>{name}</strong>,</p>
          <p style="font-size:13px;color:#555;margin-bottom:20px;line-height:1.6;">
            Your ration bill has been successfully generated at the Smart PDS shop.
            Please find the details below for your reference.
          </p>

          <!-- Bill ID box -->
          <div style="background:#e8eaf6;border:1px solid #c5cae9;border-left:4px solid #1a237e;padding:12px 16px;border-radius:2px;margin-bottom:20px;">
            <div style="font-size:12px;color:#666;">Bill Reference Number</div>
            <div style="font-size:22px;font-weight:700;color:#ff6b00;font-family:monospace;">BILL #{str(bill_id).zfill(4)}</div>
          </div>

          <!-- Items table -->
          <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
            <thead>
              <tr style="background:#1a237e;">
                <th style="padding:10px 14px;text-align:left;color:#fff;font-size:12px;font-weight:500;">Item</th>
                <th style="padding:10px 14px;text-align:left;color:#fff;font-size:12px;font-weight:500;">Quantity</th>
                <th style="padding:10px 14px;text-align:left;color:#fff;font-size:12px;font-weight:500;">Status</th>
              </tr>
            </thead>
            <tbody>
              {item_rows}
            </tbody>
            <tfoot>
              <tr style="background:#f9f9f9;">
                <td style="padding:10px 14px;font-weight:700;color:#1a237e;border-top:2px solid #1a237e;" colspan="2">Total Quantity</td>
                <td style="padding:10px 14px;font-weight:700;color:#ff6b00;font-family:monospace;border-top:2px solid #1a237e;">{total_qty} kg</td>
              </tr>
            </tfoot>
          </table>

          <!-- Kural box -->
          <div style="background:#1a237e;padding:16px;border-radius:3px;margin-bottom:20px;">
            <div style="display:inline-block;background:#ff6b00;color:#fff;font-size:10px;padding:2px 8px;border-radius:2px;font-weight:500;letter-spacing:1px;margin-bottom:8px;">THIRUKKURAL · திருக்குறள்</div>
            <div style="color:#fff;font-size:13px;line-height:1.8;">உதவி வரைத்தன்று உதவி உதவி செயப்பட்டார் சால்பின் வரைத்து</div>
            <div style="color:rgba(255,255,255,0.6);font-size:11px;font-style:italic;margin-top:6px;">"The worth of help is measured by the greatness of those who receive it." — Kural 101</div>
          </div>

          <p style="font-size:12px;color:#999;line-height:1.6;">
            This is an automated message from the Smart PDS System.<br>
            For queries, contact your nearest ration shop or district office.
          </p>

        </div>

        <!-- Footer -->
        <div style="background:#1a237e;padding:14px 28px;text-align:center;">
          <div style="height:3px;background:linear-gradient(90deg,#ff6b00 33%,#fff 33%,#fff 66%,#138808 66%);margin-bottom:10px;"></div>
          <div style="font-size:11px;color:rgba(255,255,255,0.6);">© Government of Tamil Nadu · Smart PDS System · All Rights Reserved</div>
        </div>

      </div>
    </body>
    </html>
    """