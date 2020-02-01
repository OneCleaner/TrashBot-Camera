

import socket
import sys
import numpy as np
import cv2 as cv
from PIL import Image
from io import BytesIO

cap = cv.VideoCapture(0)


while True:
    grabbed, image_np = cap.read()
    image = Image.fromarray(image_np)
    
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()

    print(type(image_bytes))

    image = np.array(Image.open(BytesIO(image_bytes)))
  

    cv.imshow('frame', image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
sys.exit()

    