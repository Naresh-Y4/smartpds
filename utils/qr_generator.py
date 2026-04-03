import qrcode
import os

def generate_qr(card_id):
    os.makedirs("static/qrcodes", exist_ok=True)
    
    qr = qrcode.make(card_id)
    path = f"static/qrcodes/{card_id}.png"
    qr.save(path)
    
    print(f"QR code saved: {path}")
    return path

# Run this once to generate QR for all your sample cards
if __name__ == '__main__':
    cards = ['TN-2024-001']  # Add more card IDs here later
    for card in cards:
        generate_qr(card)
        