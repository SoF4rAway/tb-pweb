from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from ..models.dokumen import Dokumen
from ..models.akreditasi import Akreditasi
from ..extensions import db
import os

# Create a Blueprint for documents
document_handler = Blueprint('documents', __name__)

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Upload', 'Document')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}  # Add more file extensions if needed

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@document_handler.route('/upload', methods=['GET', 'POST'])
def upload_document():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            # Handle the case where no file is selected
            return render_template('error.html', error='No file selected')

        file = request.files['file']

        # Check if the file is allowed and not empty
        if file.filename == '':
            return render_template('error.html', error='No selected file')

        if file and allowed_file(file.filename):
            # Securely save the file with a unique filename
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Create a new Dokumen instance and add it to the database
            new_document = Dokumen(
                dokumen_path=file_path,
                dokumen_name=request.form['dokumen_name'],  # Make sure you have a form field with the name 'dokumen_name'
                dokumen_label=request.form['dokumen_label']  # Make sure you have a form field with the name 'dokumen_label'
            )
            db.session.add(new_document)
            db.session.commit()

            return redirect(url_for('documents.upload_success'))

    return render_template('upload_dokumen.html')

# Add a route for success page
@document_handler.route('/upload-success')
def upload_success():
    return render_template('success.html', message='File successfully uploaded')

@document_handler.route('/download/<int:document_id>')
def download_document(document_id):
    # Fetch the Dokumen instance from the database
    document = Dokumen.query.get_or_404(document_id)

    # Return the file for download
    return send_from_directory(UPLOAD_FOLDER, os.path.basename(document.dokumen_path), as_attachment=True)
