"""Capture video and stream it to a webpage"""
# pylint: disable=no-name-in-module, unused-variable
from base64 import b64encode
from socket import AF_INET, SOCK_STREAM, gethostbyname, gethostname, socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from cv2 import VideoCapture, imencode, imshow

SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#HOST = gethostbyname(gethostname())
HOST = "192.168.1.101"
PORT = int(input("Port: "))
SOCK.bind((HOST, PORT))
print(f"{HOST}:{PORT}")
SOCK.listen(1)

STREAM0 = VideoCapture(0)
STREAM1 = VideoCapture(2)
STREAM0.set(3, 320)
STREAM0.set(4, 240)
STREAM1.set(3, 320)
STREAM1.set(4, 240)
#STREAM1 = STREAM0
#STREAM0 = STREAM1

def server():
"""Stream live video"""
ret0, frame0 = STREAM0.read()
ret1, frame1 = STREAM1.read()
try:
retval0, buffer0 = imencode('.jpg', frame0)
retval1, buffer1 = imencode('.jpg', frame1)
server_thread = Thread(target=server, daemon=True)
conn, addr = SOCK.accept()
server_thread.start()
except Exception:
return
#imshow("frame0", frame0)
#imshow("frame1", frame1)
try:
data = conn.recv(512).decode().split(' ')
if data[0] == "GET":
with open("stream.html", "rb") as website:
conn.sendall(b"HTTP/1.1 200 OK\n\n" + website.read())
elif data[0] == "VIDEO0":
conn.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(buffer0))
elif data[0] == "VIDEO1":
conn.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(buffer1))
except ConnectionResetError:
return
conn.close()


server()
from time import sleep
while True:
try:
sleep(20)
except KeyboardInterrupt:
SOCK.close()
break
STREAM0.release()
STREAM1.release()
