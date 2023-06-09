import imutils
import cv2
import easyocr
import pytesseract
import os


def get_license_plate_from_image(image_name):
    image_path = image_name.split('.')[0]
    image = cv2.imread(image_name)
    os.remove(image_name)
    # resize the image
    image = imutils.resize(image, width=500)

    # grayscale the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # smooth the image
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # gets the edges from the grayscaled image
    edged = cv2.Canny(gray, 170, 200)

    # find the contours
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    number_plate_count = None

    count = 0
    name = 0
    filename = f'{image_path}_RECOGNIZED.png'
    #  Takes the the rectangle with the most area
    for i in cnts:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(i)
            crp_image = image[y:y + h, x:x + w]
            name += 1
            cv2.imwrite(filename, crp_image)
            break
    if name < 1:
        return False
    cropped = cv2.imread(filename)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped)
    if not result:
        return False
    return result[0][1]


def get_digits(string: str):
    if not string:
        return ''
    return ''.join(list(filter(lambda x: x.isdigit(), string)))


def recognize_from_image(image_name: str):
    return get_digits(get_license_plate_from_image(image_name))
