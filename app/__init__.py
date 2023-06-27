from flask import Flask  
from config import Config
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config.from_object(Config)
db = SQLAlchemy(app)
cloud=cloudinary.config(
    cloud_name = "kmalifdev",
    api_key = "812952289488894",
    api_secret = "2BoMB5qbjwpnWACUtEATXoTmYao"
)
jwt = JWTManager(app)



from app.models import mitraModel,userModel, newsModel, recomendationsModel
from app import routes