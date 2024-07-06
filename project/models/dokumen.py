from datetime import datetime
from ..extensions import db

class Dokumen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    dokumen_path = db.Column(db.Text)
    dokumen_name = db.Column(db.Text)
    dokumen_label = db.Column(db.String(255))  # Adjust the length based on your needs

    def __init__(self, dokumen_path, dokumen_label, dokumen_name):
        self.dokumen_path = dokumen_path
        self.dokumen_label = dokumen_label
        self.dokumen_name = dokumen_name
