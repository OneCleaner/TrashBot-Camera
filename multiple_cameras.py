import cv2 as cv

video_capture_0 = cv.VideoCapture(0)
video_capture_1 = cv.VideoCapture(2)

while True:
    ret0, frame0 = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()

    if (ret0):
        cv.imshow('Cam 0', frame0)

    if (ret1):
        cv.imshow('Cam 1', frame1)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture_0.release()
video_capture_1.release()
cv.destroyAllWindows()
