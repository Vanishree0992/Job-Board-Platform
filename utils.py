import os
from flask import current_app
from werkzeug.utils import secure_filename

def save_resume(file_storage):
    fn = secure_filename(file_storage.filename)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], fn)
    file_storage.save(path)
    return fn
