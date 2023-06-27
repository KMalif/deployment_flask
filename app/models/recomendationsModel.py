from app import db


class Recomendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bentuk = db.Column(db.String(100))
    image = db.Column(db.Text)
    gender = db.Column(db.String(100))
    panjangrambut = db.Column(db.String(50))
    nama_model = db.Column(db.String(100))
    content = db.Column(db.Text)

    def __init__(self, bentuk, image, gender, panjangrambut, nama_model, content):
        self.bentuk = bentuk
        self.image = image
        self.gender = gender
        self.panjangrambut = panjangrambut
        self.nama_model = nama_model
        self.content = content
