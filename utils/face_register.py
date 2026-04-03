import cv2
import os
from utils.db import execute_query

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def register_face(member_id):
    """
    Opens webcam, captures face, saves image, updates DB.
    """
    os.makedirs("static/faces", exist_ok=True)

    cap = cv2.VideoCapture(0)
    print(f"Registering face for member {member_id}")
    print("Press SPACE to capture, ESC to cancel")

    saved_path = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected!", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, "Press SPACE to capture", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Face Registration", frame)

        key = cv2.waitKey(1)

        if key == 32:  # SPACE
            if len(faces) == 0:
                print("No face detected! Please try again.")
                continue

            # Save the face image
            path = f"static/faces/member_{member_id}.jpg"
            cv2.imwrite(path, frame)

            # Update DB
            execute_query(
                "UPDATE family_members SET face_image_path = %s WHERE member_id = %s",
                (path, member_id)
            )
            print(f"Face saved at {path} and DB updated!")
            saved_path = path
            break

        elif key == 27:  # ESC
            print("Registration cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return saved_path


if __name__ == '__main__':
    print("=== Face Registration ===")
    print("1 - Ravi Kumar")
    print("2 - Priya Kumar")
    print("3 - Arjun Kumar")
    member_id = int(input("Enter member ID to register: "))
    result = register_face(member_id)
    if result:
        print(f"✅ Registration successful: {result}")
    else:
        print("❌ Registration failed")