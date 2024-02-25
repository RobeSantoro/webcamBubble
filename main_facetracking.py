import cv2


def detect_faces(img):
    face_cascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')  # Load the face detection model
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
    return faces


def draw_bounding_box(img, faces):
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


def center_faces(img, faces):
    if len(faces) == 1:
        x, y, w, h = faces[0]
        cx, cy = x + w // 2, y + h // 2
        width, height = img.shape[:2]
        delta_x = (width - w) // 2
        delta_y = (height - h) // 2
    else:
        return img

    result = cv2.copyMakeBorder(
        img, delta_y, delta_y, delta_x, delta_x, cv2.BORDER_CONSTANT, value=0)
    return result


def main():
    cap = cv2.VideoCapture(0)  # Use the default webcam

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        faces = detect_faces(frame)
        draw_bounding_box(frame, faces)
        result = center_faces(frame, faces)

        cv2.imshow('Face Tracker', result)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
