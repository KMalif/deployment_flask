from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.userModel import Users
from app.models.wishlistModel import db, Wishlist
from datetime import date, datetime
from sqlalchemy import desc


ma = Marshmallow(app)

class WishlistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_user', 'image', 'nama_model', 'content', 'date')


wishlistSchema = WishlistSchema()
wishlistsSchema = WishlistSchema(many=True)

def postWishlist(decodeToken):
    data = request.get_json()
    id_user = decodeToken.get('id_user')
    image = data['image']
    nama_model = data['nama_model']
    content = data['content']
    tanggal = date.today()
    newWishlist = Wishlist(id_user, image, nama_model, content, tanggal)
    db.session.add(newWishlist)
    db.session.commit()
    new = wishlistSchema.dump(newWishlist)
    return jsonify({"msg": "Success add wishlist", "status": 200, "data": new})

def getAllWishlist(decodeToken):
    id_user = decodeToken.get('id_user')
    wishlistsQuery = Wishlist.query.with_entities(Wishlist.id, Wishlist.id_user, Wishlist.image, Wishlist.nama_model, Wishlist.content, Wishlist.date).filter(Wishlist.id_user == id_user).order_by(desc(Wishlist.date))
    wishlists = wishlistsSchema.dump(wishlistsQuery)
    return jsonify({"msg": "Success get wishlist by id", "status": 200, "data": wishlists})

def deleteWishlist(id):
    wishlist = Wishlist.query.get(id)
    db.session.delete(wishlist)
    db.session.commit()
    wishlistDelete = wishlistSchema.dump(wishlist)
    return jsonify({"msg": "Success Delete wishlist", "status": 200, "data": wishlistDelete})

