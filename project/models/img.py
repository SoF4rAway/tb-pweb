from ..extensions import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.Text)  # Adjust the data type if needed

    def __init__(self, img_path, berita):
         self.img_path = img_path
         self.berita = berita
