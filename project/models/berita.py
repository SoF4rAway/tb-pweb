from datetime import datetime
from ..extensions import db

class Berita(db.Model):
    berita_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    # Foreign Key to User table
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    author = db.relationship('User', backref=db.backref('berita', lazy=True))

    # Relationship with Berita_img
    images = db.relationship('Berita_img', back_populates='berita', lazy=True)

    def __repr__(self):
        return f"<Berita {self.berita_id}: {self.title}>"
