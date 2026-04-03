import cv2

def scan_qr_from_webcam():
    """
    Opens webcam and scans for QR code using OpenCV (no pyzbar needed).
    Returns the card_id string when detected.
    """
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    print("Webcam open — show QR code to camera. Press ESC to cancel.")

    card_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            card_id = data
            cv2.putText(frame, f"Detected: {card_id}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("QR Scanner", frame)
            cv2.waitKey(1000)
            break

        cv2.putText(frame, "Show QR Code to camera...", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("QR Scanner", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
    return card_id