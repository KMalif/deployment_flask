from app import db


class Hair(db.Model):
    id_hair = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    nama_model = db.Column(db.String(200))
    content = db.Column(db.Text)

    def __init__(self, image, nama_model, content):
        self.image = image
        self.nama_model = nama_model
        self.content = content
