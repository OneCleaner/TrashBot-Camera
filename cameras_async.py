import cv2 as cv
from threading import Thread
import sys


class WebcamStream(object):

    # costruttore inutile ma io lo metto
    def __new__(cls, *args, **kwargs):
        return super(WebcamStream, cls).__new__(cls)

    def __init__(self, src=0, mirror=False, size=1):

        self.stream = cv.VideoCapture(src)
        self.mirror = mirror
        self.size = size
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False
        self.__thread = Thread(target=self.update, args=())

    def start(self):
        # parte il thread, possiamo definire l'oggetto per poi farlo partire in un secondo momento
        # o passare il thread già istanziato
        self.__thread.start()
        return self

    def update(self):
        # legge e manda i frame appena sono disponibili
        while True:
            # ci fermiamo se il ci viene indicato.
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # ritorna la roba ultima presa
        return self.grabbed, self.frame

    def jpg(self):
        ret, jpg = cv.imencode('.jpg', self.frame, [int(cv.IMWRITE_JPEG_QUALITY), 95])
        return jpg.tobytes()

    def stop(self):
        # possiamo fermare il thread in esecuzione ma non fermarlo, a differenza dei processi
        self.stopped = True

    def get_stream(self):
        return self.stream


if __name__ == "__main__":

    # istanziamo le classi e i thread
    web_1 = WebcamStream(src=0, mirror=True)
    web_1.start()
    web_2 = WebcamStream(src=1, mirror=True)
    web_2.start()

    while True:
        # grabbiamo i frame dai processi in esecuzione
        grabbed_1, frame_1 = web_1.read()
        grabbed_2, frame_2 = web_2.read()

        if web_1.mirror:
            frame_1 = cv.flip(frame_1, 1)

        if web_2.mirror:
            frame_2 = cv.flip(frame_2, 1)

        frame_1 = cv.resize(frame_1, None, fx=web_1.size, fy=web_1.size, interpolation=cv.INTER_AREA)
        frame_2 = cv.resize(frame_2, None, fx=web_2.size, fy=web_2.size, interpolation=cv.INTER_AREA)

        cv.imshow('webcam 1', frame_1)
        cv.imshow('webcam 2', frame_2)
        if (cv.waitKey(1) == 27) | (cv.waitKey(1) & 0xFF == ord('q')):  # ESC o Q per uscire
            break

    web_1.stop()
    web_2.stop()
    cv.destroyAllWindows()
    sys.exit()
