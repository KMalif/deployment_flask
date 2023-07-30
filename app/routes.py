from app import app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import hairModel, mitraController, newsController, userController, wishlistController


@app.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def userDetails():
    current_user = get_jwt_identity()
    if(request.method == 'GET'):
        return userController.getDetailUser(current_user)
    if(request.method == 'PUT'):
        return userController.updateUser(current_user)


@app.route('/signup', methods=['POST'])
def signUp():
    return userController.signUp()


@app.route('/signin', methods=['POST'])
def signIn():
    return userController.signIn()


@app.route('/mitra', methods=['POST', 'GET', 'PUT'])
@jwt_required()
def mitra():
    payload_user = get_jwt_identity()
    if(request.method == 'POST'):
        return mitraController.postMitra()
    elif(request.method == 'PUT'):
        return mitraController.updateMitra(payload_user)
    elif (request.method == 'GET'):
        return mitraController.getAllMitra()


@app.route('/mitraDetails', methods=["GET"])
@jwt_required()
def mitraDetails():
    payload_user = get_jwt_identity()
    return mitraController.getMitraDetails(payload_user)


@app.route('/mitra/<id>', methods=['GET', 'DELETE'])
@jwt_required()
def mitraById(id):
    if(request.method == 'GET'):
        return mitraController.getMitraById(id)
    elif (request.method == 'DELETE'):
        return mitraController.deleteMitra(id)

@app.route('/predict', methods=['POST'])
@jwt_required()
def prediksi():
    if(request.method == 'POST'):
        return recomendationsController.predict()
    elif(request.method == 'GET'):
        return recomendationsController.getAllRecomendation()

@app.route('/recomendations', methods=['POST', 'GET'])
def recomendations():
    if(request.method == 'POST'):
        return recomendationsController.postRecomendations()
    elif(request.method == 'GET'):
        return recomendationsController.getAllRecomendation()

@app.route('/recomendations/<id>', methods=['GET'])
@jwt_required()
def detailRecomendation(id):
    return recomendationsController.getRecomendationById(id)


@app.route('/news', methods=['POST', 'GET'])
@jwt_required()
def newsRoute():
    if(request.method == 'POST'):
        return newsController.postNews()
    elif(request.method == 'GET'):
        return newsController.getAllNews()


@app.route('/news/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def newsRouteById(id):
    if(request.method == 'GET'):
        return newsController.getNewsById(id)
    if(request.method == 'PUT'):
        return newsController.updateNews(id)
    if(request.method == 'DELETE'):
        return newsController.deleteNews(id)


@app.route('/hairmodel', methods=['POST', 'GET'])
@jwt_required()
def hairModelRoutes():
    if(request.method == 'POST'):
        return hairModel.postHairModel()
    elif(request.method == 'GET'):
        return hairModel.getAllHairModel()

@app.route('/whistlist', methods=['POST', 'GET'])
@jwt_required()
def wishlistRoutes():
    payload_user = get_jwt_identity()
    if(request.method == 'POST'):
        return wishlistController.postWishlist(payload_user)
    elif(request.method == 'GET'):
        return wishlistController.getAllWishlist(payload_user)


@app.route('/whistlist/<id>', methods=['DELETE'])
@jwt_required()
def wishlistRoutesbyId(id):
    return wishlistController.deleteWishlist(id)
    
