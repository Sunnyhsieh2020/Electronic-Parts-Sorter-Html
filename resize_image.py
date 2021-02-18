import cv2

img = cv2.imread("./static/unnamed.jpg", cv2.IMREAD_COLOR)

img = cv2.resize(img, (1503, 1000))
cv2.imwrite("./static/unnamed.jpg", img)
cv2.waitKey(0)
