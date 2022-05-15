import matplotlib.pyplot as plt
import keras_ocr
import numpy as np
import cv2
import math

pipeline = keras_ocr.pipeline.Pipeline()
# read image from the an image path (a jpg/png file or an image url)
#img = keras_ocr.tools.read('download/stills/9QGjhPp2Gjs.2/001.jpg')
# Prediction_groups is a list of (word, box) tuples
#prediction_groups = pipeline.recognize([img])
# print image with annotation and boxes


def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)


def inpaint_text(img_path, pipeline):
    # read image
    img = keras_ocr.tools.read(img_path)
    # generate (word, box) tuples
    prediction_groups = pipeline.recognize([img])
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1]
        x2, y2 = box[1][2]
        x3, y3 = box[1][3]

        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)

        thickness = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,
                 thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

    return img


img = inpaint_text('download/stills/9QGjhPp2Gjs.2/001.jpg', pipeline)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imwrite('text_free_image.jpg', img_rgb)
