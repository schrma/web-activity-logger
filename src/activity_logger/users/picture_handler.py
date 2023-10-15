import os
import cv2 as cv
import numpy

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' +ext_type

    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)

    # Play Around with this size.
    output_size = (200, 200)

    # Open the picture and save it
    filestr = pic_upload.read()
    file_bytes = numpy.fromstring(filestr, numpy.uint8)
    img = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)
    img_thumb = cv.resize(img, dsize=output_size, interpolation=cv.INTER_CUBIC)
    cv.imwrite(filepath, img_thumb)
    #pic = Image.open(pic_upload)
    #pic.thumbnail(output_size)
    #pic.save(filepath)

    return storage_filename
