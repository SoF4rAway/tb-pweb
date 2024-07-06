# models/dosen.py
from ..extensions import db

class Dosen(db.Model):
    nip = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nama = db.Column(db.Text)
    sinta = db.Column(db.Text)
    scopus = db.Column(db.Text)
    departemen = db.Column(db.Text)
    jabatan = db.Column(db.Text)
    profile_img = db.Column(db.Text)  # Assuming the image path or URL will be stored as text

    def __init__(self, nip, nama, sinta, scopus, departemen, jabatan, profile_img):
        self.nip = nip
        self.nama = nama
        self.sinta = sinta
        self.scopus = scopus
        self.departemen = departemen
        self.jabatan = jabatan
        self.profile_img = profile_img