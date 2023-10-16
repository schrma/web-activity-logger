import os
import cv2 as cv
import numpy as np

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' +ext_type

    filepath = os.path.join(current_app.root_path, r"static/profile_pics", storage_filename)

    # Play Around with this size.
    output_size = (200, 200)

    # Open the picture and save it
    filestr = pic_upload.read()
    file_bytes = np.fromstring(filestr, np.uint8)

    img = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv.imdecode(img, cv.IMREAD_UNCHANGED)
    img_thumb = cv.resize(img, dsize=output_size, interpolation=cv.INTER_CUBIC)
    if (cv.imwrite(filepath, img_thumb)):
        print(f"\nCould write to {filepath}")
    else:
        print(f"\nERROR: Could not write to {filepath}")

    return storage_filename
