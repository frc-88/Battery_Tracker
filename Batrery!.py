import cv2

capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    success, image = capture.read()
    if not success:
        print("Could not access the camera")
        break
    debug_image = image
    success, qrcode_data, qrcode_points, straight_qrcode = detector.detectAndDecodeMulti(image)
    if success:
        for data, bbox in zip(qrcode_data, qrcode_points):
            if data.startswith("tj2-battery"):
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            bbox = bbox.astype(int)
            debug_image = cv2.polylines(image, [bbox], True, color, 2)
            debug_image = cv2.putText(
                debug_image,
                data,
                (int(bbox[0, 0]), int(bbox[0, 1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2,
                cv2.LINE_AA,
            )
    cv2.imshow("QR Code Scanner", debug_image)
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break