from sassandsass import app
from os import path, listdir

allowed_extensions = ('jpg', 'png', 'gif', ".tiff")

def is_web_image(imagename):
    return '.' in imagename and \
            imagename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_image(img):
    if img and is_web_image(img.filename):
        filename = secure_filename(img.filename)
        img.save(path.join(app.config['IMAGE_FOLDER'], filename))
        return filename
    else:
        return None

def get_available_images():
    return [imagename for imagename in listdir(app.config["IMAGE_FOLDER"])
            if is_web_image(imagename)]
