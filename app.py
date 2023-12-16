import os

# Import flask modules
from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
# Import my modules
import main





app = Flask(__name__)

app.config['SECRET_KEY'] = 'solving_the_sudoku'

path = 'static/temp'

# Set the path of the uploaded images
app.config['UPLOADED_PHOTOS_DEST'] = path

# Configure the format that I want to upload
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Create a form to validate the user input
class UploadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload Sudoku Image')

@app.route(f'/{path}/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    # Remove all cache
    if os.listdir(path):
        for name in os.listdir(path):
            file = f"{path}/{name}"            
            if os.path.isfile(file):
                os.remove(file)

    # Create an instance of the form class
    form = UploadForm()
    # Validate the upload of image
    if form.validate_on_submit():
        # Save the file (image)
        filename = photos.save(form.photo.data)
        # Get the original image
        file_url = url_for('get_file', filename=filename)
        # Solved sudoku
        images = main.solver(filename)
        # Save every url of the image in a variable
        images_url = [ url_for('get_file', filename=image) for image in images]
        
    else:
        file_url, images_url = None, None

    return render_template("index.html",
                           form=form,
                           file_url=file_url,
                           images=images_url)