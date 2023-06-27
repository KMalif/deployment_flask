from app import db
from sqlalchemy.sql import func

from app.models.userModel import Users


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id_user))
    image = db.Column(db.String(200))
    nama_model = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.Date)

    def __init__(self, id_user, image, nama_model, content, date):
        self.id_user = id_user
        self.image = image
        self.nama_model = nama_model
        self.content = content
        self.date = date