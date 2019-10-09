"""Capture video and stream it to a webpage"""
#pylint: disable=no-name-in-module
from base64 import b64encode
from socket import AF_INET, SOCK_STREAM, socket, gethostbyname, gethostname
import sys
import cv2 as cv

SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind((gethostbyname(gethostname()), 7503))
SOCK.listen(1)

STREAM0 = cv.VideoCapture(0)
STREAM1 = cv.VideoCapture(1)


while True:
    RET0, FRAME0 = STREAM0.read()
    RET1, FRAME1 = STREAM1.read()
    RETVAL0, BUFFER0 = cv.imencode('.jpg', FRAME0)
    RETVAL1, BUFFER1 = cv.imencode('.jpg', FRAME1)
    CONN, ADDR = SOCK.accept()
    DATA = CONN.recv(512).decode().split(' ')
    if DATA[0] == "GET":
        with open("test.html", "rb") as website:
            CONN.sendall(b"HTTP/1.1 200 OK\n\n" + website.read())
    elif DATA[0] == "VIDEO0":
        CONN.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(BUFFER0))
    elif DATA[0] == "VIDEO1":
        CONN.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(BUFFER1))
    CONN.close()
    cv.imshow('frame0', FRAME0)
    cv.imshow('frame1', FRAME1)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
STREAM0.release()
STREAM1.release()
cv.destroyAllWindows()
sys.exit()
