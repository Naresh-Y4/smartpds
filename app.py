from flask import Flask, render_template, jsonify, session
from config import SECRET_KEY
from routes.auth import auth_bp
from routes.members import members_bp
from routes.face import face_bp
from routes.billing import billing_bp
from routes.qr import qr_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register all blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(members_bp, url_prefix='/api')
app.register_blueprint(face_bp, url_prefix='/api/face')
app.register_blueprint(billing_bp, url_prefix='/api')
app.register_blueprint(qr_bp, url_prefix='/api/qr')

# ── Page Routes ──────────────────────────────────────────
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/scan')
def scan_page():
    return render_template('scan.html')

@app.route('/members')
def members_page():
    return render_template('members.html')

@app.route('/verify')
def verify_page():
    return render_template('verify.html')

@app.route('/billing')
def billing_page():
    return render_template('billing.html')

# ── Extra API helpers ────────────────────────────────────
@app.route('/api/auth/session')
def get_session():
    return jsonify({
        'shop_id': session.get('shop_id'),
        'shop_name': session.get('shop_name')
    })

if __name__ == '__main__':
    app.run(debug=True)