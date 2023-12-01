import cv2

capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    success, image = capture.read()
    if not success:
        print("Could not access the camera")
        break
    data, bbox, _ = detector.detectAndDecode(image)
    if data:
        print(data)
        debug_image = cv2.polylines(image, [bbox.astype(int)], True, (0, 255, 0), 2)
    else:
        debug_image = image
    cv2.imshow("QR Code Scanner", debug_image)
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break