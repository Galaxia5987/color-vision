import cv2 as cv

from app.camera.color_detector import ColorDetector

def main():
    camera = cv.VideoCapture(0)
    detector = ColorDetector([61,48,43], [103,255,255])

    while True:
        _, frame = camera.read()

        objects, mask = detector.proccess(frame)
        print(objects)
        annotated_frame = detector.annotate_frame(frame, objects)
        cv.imshow('Annotated Stream', annotated_frame)
        cv.imshow('Mask', mask)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()