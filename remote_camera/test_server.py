import platform
import socket
import cv2 as cv
from PIL import Image
from io import BytesIO
import numpy as np
from time import sleep


def server(indirizzo, backlog=1):
    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #apriamo la comunicazione tramite socket
        skt.bind(indirizzo)
        skt.listen(backlog)
        print("Server seriale inizializzato. In ascolto... ")
    except socket.error as errore:     #se esplode tutto ci si riprova
        print("Qualcosa è andato storto: \n" + str(errore))
        print("Reinizialiazzazione Server in corso...")
        server(indirizzo, kit, serial, backlog=1)
    else:   #se non esplode stabiliamo la connessione
        conn, indirizzo_client = skt.accept()  # conn = socket_client
        print("Connessione Server - Client Stabilita: " + str(indirizzo_client))
        while True:
            image_bytes = conn.recv(4096000)
            image_np = np.array(Image.open(BytesIO(image_bytes)))
        
            cv.imshow('frame', image_np)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()
        sys.exit()

            


if __name__ == "__main__":  #eseguiamo soltanto se questa è la classe main

    server(("", int(30027)), backlog=1)

