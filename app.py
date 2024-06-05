from flask import Flask, render_template, request, jsonify
import cv2
from matplotlib import pyplot as plt
import numpy as np
import pytesseract
import imutils
import csv
import uuid

app = Flask(__name__)

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def home1():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/process', methods=['POST'])
def process():
    # Assuming you upload an image via a form
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Your existing image processing code
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    keypoints = cv2.findContours(erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)

    min_area = 500
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    filtered_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in filtered_contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    result_text = ""
    if location is not None:
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))

        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        result_text = text.strip()

        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=result_text, org=(location[0][0][0], location[1][0][1] - 15), fontFace=font, fontScale=1, color=(0, 0, 255), thickness=4, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)

        # Generate a unique filename for the output image
        output_image_filename = str(uuid.uuid4()) + '.jpg'
        # Save the final image with the unique filename
        cv2.imwrite('static/' + output_image_filename, res)

        # Save the recognized text to a CSV file
        csv_file = "Output_text.csv"
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                lines = list(reader)
                serial_number = len(lines)
        except FileNotFoundError:
            serial_number = 1

        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Recognized Text_" + str(serial_number)])
            writer.writerow([result_text])

    return jsonify(result=result_text, image_url='static/' + output_image_filename)

if __name__ == '__main__':
    app.run(debug=True)
