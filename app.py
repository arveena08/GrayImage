# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np


app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')


# Function to upload image and redirect to new webpage
@app.route('/gray', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)

    file_data = make_grayscale(file.read())
    with open(os.path.join('static/', filename), 'wb') as f:
        f.write(file_data)
    

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)


def make_grayscale(input):
    image_array = np.fromstring(input , dtype='uint8')
    print('Image array :', image_array)

    #decode array into an image
    decode_artoimg =cv2.imdecode(image_array , cv2.IMREAD_UNCHANGED)
    print('decoded values of image : ', decode_artoimg)

    #Make grayscale
    converted_grayimg = cv2.cvtColor(decode_artoimg , cv2.COLOR_RGB2GRAY)
    status , output_img = cv2.imencode('.PNG' , converted_grayimg)
    print('Status :' , status)
    return(output_img)

    
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))


if __name__ == "__main__":
    app.run()


