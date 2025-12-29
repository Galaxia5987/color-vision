import cv2


def frames_to_jpeg_bytes(frame, resolution=(640, 480)):
    resized = cv2.resize(frame, resolution)
    ret, jpeg = cv2.imencode(".jpg", resized)
    if not ret:
        return None
    return jpeg.tobytes()