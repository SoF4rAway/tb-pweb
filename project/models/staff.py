# models/staff.py
from ..extensions import db

class Staff(db.Model):
    nip = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nama = db.Column(db.Text)
    jabatan = db.Column(db.Text)
    profile_img = db.Column(db.Text)  # Assuming the image path or URL will be stored as text

    def __init__(self, nip, nama, jabatan, profile_img):
        self.nip = nip
        self.nama = nama
        self.jabatan = jabatan
        self.profile_img = profile_img