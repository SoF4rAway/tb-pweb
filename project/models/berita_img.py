from ..extensions import db
from .berita import Berita  # Import the Berita model

class Berita_img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.Text)  # Adjust the data type if needed
    berita_id = db.Column(db.Integer, db.ForeignKey('berita.berita_id'), nullable=False)
    berita = db.relationship('Berita', back_populates='images', lazy=True)

    def __init__(self, img_path, berita):
        self.img_path = img_path
        self.berita = berita
