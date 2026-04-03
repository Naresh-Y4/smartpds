import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_and_verify(stored_image_path):
    """
    Opens webcam, captures live face, compares with stored image.
    Returns True if match, False otherwise.
    """
    if not os.path.exists(stored_image_path):
        return False, "Stored image not found"

    stored_img = cv2.imread(stored_image_path, cv2.IMREAD_GRAYSCALE)
    stored_face = detect_face(stored_img)
    if stored_face is None:
        return False, "No face found in stored image"

    cap = cv2.VideoCapture(0)
    matched = False
    message = "Face not matched"

    print("Webcam open — press SPACE to capture, ESC to cancel")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Face Verification — Press SPACE to capture", frame)

        key = cv2.waitKey(1)

        if key == 32:  # SPACE key
            live_face = detect_face(gray)
            if live_face is not None:
                score = compare_faces(stored_face, live_face)
                print(f"Match score: {score}")
                if score < 80:  # Lower = more similar in LBPH
                    matched = True
                    message = "Face matched successfully"
                else:
                    message = f"Face not matched (score: {score:.1f})"
            else:
                message = "No face detected in frame"
            break

        elif key == 27:  # ESC key
            message = "Verification cancelled"
            break

    cap.release()
    cv2.destroyAllWindows()
    return matched, message


def detect_face(gray_img):
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    face = gray_img[y:y+h, x:x+w]
    return cv2.resize(face, (200, 200))


def compare_faces(face1, face2):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Train with stored face as label 0
    recognizer.train([face1], np.array([0]))
    label, confidence = recognizer.predict(face2)
    return confidence


def save_face_image(member_id, image_data):
    """Save uploaded face image to static/faces/"""
    path = f"static/faces/member_{member_id}.jpg"
    os.makedirs("static/faces", exist_ok=True)
    with open(path, 'wb') as f:
        f.write(image_data)
    return path