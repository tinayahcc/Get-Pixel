from gpiozero import RGBLED
import numpy as np
import cv2

led = RGBLED(9,10,11)

COLOR_ROWS = 80
COLOR_COLS = 250
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
if not cap.isOpened():
    raise RuntimeError('Error opening VideoCapture.')

colorArray = np.zeros((COLOR_ROWS, COLOR_COLS, 3), dtype=np.uint8)

while True:
    (grabbed, frame) = cap.read()
    height, width = frame.shape[:2]

    cv2.circle(frame,(int(width/2),int(height/2)), 20, (0,0,255), 0)
    cv2.imshow('Video', frame)

    if not grabbed:
        break
    
    KeyVal = cv2.waitKey(1) &0xFF
    if KeyVal == ord('e'):
        break

    snapshot = frame.copy()

    colorArray[:] = snapshot[int(height/2), int(width/2), :]
    rgb = snapshot[int(height/2), int(width/2), [2,1,0]]

    luminance = 1 - (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) / 255
    if luminance < 0.5:
        textColor = [0,0,0]
    else:
        textColor = [255,255,255]

    cv2.putText(colorArray, str(rgb), (20, COLOR_ROWS - 20),
    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=textColor)
    cv2.imshow('Color', colorArray)
    
    r = 1 - (rgb[0] / 255)
    g = 1 - (rgb[1] / 255)
    b = 1 - (rgb[2] / 255)
    led.color=(r,g,b)

cap.release()
cv2.destroyAllWindows()
