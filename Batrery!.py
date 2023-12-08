import cv2
import pandas as pd
import os

#capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

filenames = os.listdir('./data')

def process_image(image):
    '''Process an image looking for QR codes.
    Args:
        image: a numpy array with shape (rows, columns, 3)
    Returns:
        debug_image: a numpy array with shape (rows, columns, 3)'''
    debug_image = image
    success, qrcode_data, qrcode_points, straight_qrcode = detector.detectAndDecodeMulti(image)
    if success:
        for data, bbox in zip(qrcode_data, qrcode_points):
            registered = False
            for filename in filenames: 
                registered = False
                if filename.startswith(data) and filename.endswith(".csv"):
                     registered = True
                     break
            if(registered == False):
                color = (0, 0, 255)
                print("unrigestered battery detected")
            elif(registered == True):
                color = (0, 255, 0)
                print("rigestered battery detected")
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
    return  debug_image

# while True:
#     success, image = capture.read()
#     if not success:
#         print("Could not access the camera")
#         break

image = cv2.imread('./images/tj2-battery4.jpg')
debug_image = process_image(image)

#next we need to load the csv file
#read the data from the csv file
#use csv data to calculate dr.J math stuff (numerical integrals)



cv2.imshow("QR Code Scanner", debug_image)
key = chr(cv2.waitKey(-1) & 0xFF)


    