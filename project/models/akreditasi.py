from datetime import datetime
from ..extensions import db

class Akreditasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_started = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    lembaga = db.Column(db.Text)
    peringkat = db.Column(db.Text)
    dokumen = db.Column(db.Text)
    dokumen_path = db.Column(db.Text)
    departemen = db.Column(db.Text)

    def __init__(self, lembaga, peringkat, dokumen, dokumen_path, departemen, date_started, date_end):
        self.lembaga = lembaga
        self.peringkat = peringkat
        self.dokumen = dokumen
        self.dokumen_path = dokumen_path
        self.departemen = departemen
        self.date_started = date_started
        self.date_end = date_end
