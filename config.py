import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "containers-us-west-108.railway.app"
    DATABASE = "railway"
    USERNAME = "root"
    PASSWORD = "mHnpRujeIZDFa03XWQa1"
    PORT = "6487"
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
    # SQLALCHEMY_DATABASE_URI = 'postgresql://keyhjbritoyqcj:804aadb24179eb9cbee788f80dea8929dd5d41030c271942fefb01f488d35ec4@ec2-35-173-83-57.compute-1.amazonaws.com:5432/dek1mr5jkf2kj9'
    # SQLALCHEMY_DATABASE_URI = mysql -hcontainers-us-west-108.railway.app -uroot -pmHnpRujeIZDFa03XWQa1 --port 6487 --protocol=TCP railway
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # HOST = "localhost"
    # DATABASE = "cutbox"
    # USERNAME = "root"
    # PASSWORD = "alif19090068"
    # JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    # SQLALCHEMY_DATABASE_URI = 'mysql://'+USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE
    # # SQLALCHEMY_DATABASE_URI = 'postgresql://keyhjbritoyqcj:804aadb24179eb9cbee788f80dea8929dd5d41030c271942fefb01f488d35ec4@ec2-35-173-83-57.compute-1.amazonaws.com:5432/dek1mr5jkf2kj9'

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True
