import cv2 as cv2
print(cv2.__version__)
import numpy as np

video = cv2.VideoCapture(0)
_, frame = video.read()
# cv2.imshow("First Frame", frame)
# x = 260
# y = 90
# height = 100
# width = 100
(x, y, width, height) = cv2.selectROI(frame, False)
roi = frame[y: y + height, x: x + width]
cv2.imshow("Mask", roi)
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    _, frame = video.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    _, track_window = cv2.meanShift(mask, (x, y, width, height), term_criteria)
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(60)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()