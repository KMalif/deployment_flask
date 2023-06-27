from app import app
from app import cloud
from flask import request, jsonify
from flask_marshmallow import Marshmallow
import tensorflow as tf
from tensorflow.keras.models import load_model
from mtcnn.mtcnn import MTCNN
import cv2
import urllib.request
import numpy as np
import cloudinary.uploader
import os
from werkzeug.utils import secure_filename
from app.models.recomendationsModel import db, Recomendations

ma = Marshmallow(app)


class RecomenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'bentuk', 'image', 'gender', 'score', 'panjangrambut', 'nama_model', 'content')


rekomens_schema = RecomenSchema()
rekomen_schema = RecomenSchema(many=True)


basedir = os.path.abspath(os.path.dirname(__file__))


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#model 
with open('model/faceshape_model.json', 'r') as json_file:
    json_savedModel = json_file.read()

model = tf.keras.models.model_from_json(json_savedModel)
# model = load_model(
#     'model/vgg16-face-1/')
detector = MTCNN()


def crop_and_resize(image, target_w=224, target_h=224):
    if image.ndim == 2:
        img_h, img_w = image.shape
    elif image.ndim == 3:
        img_h, img_w, channels = image.shape
    target_aspect_ratio = target_w/target_h
    input_aspect_ratio = img_w/img_h

    if input_aspect_ratio > target_aspect_ratio:
        resize_w = int(input_aspect_ratio*target_h)
        resize_h = target_h
        img = cv2.resize(image, (resize_w, resize_h))
        crop_left = int((resize_w - target_w)/2)
        crop_right = crop_left + target_w
        new_img = img[:, crop_left:crop_right]
    if input_aspect_ratio < target_aspect_ratio:
        resize_w = target_w
        resize_h = int(target_w/input_aspect_ratio)
        img = cv2.resize(image, (resize_w, resize_h))
        crop_top = int((resize_h - target_h)/4)
        crop_bottom = crop_top + target_h
        new_img = img[crop_top:crop_bottom, :]
    if input_aspect_ratio == target_aspect_ratio:
        new_img = cv2.resize(image, (target_w, target_h))

    return new_img


def extract_face(img, target_size=(224, 224)):
    results = detector.detect_faces(img)
    if results == []:
        new_face = crop_and_resize(img, target_w=224, target_h=224)
    else:
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1+width, y1+height
        face = img[y1:y2, x1:x2]
        adj_h = 10
        if y1-adj_h < 10:
            new_y1 = 0
        else:
            new_y1 = y1-adj_h
        if y1+height+adj_h < img.shape[0]:
            new_y2 = y1+height+adj_h
        else:
            new_y2 = img.shape[0]
        new_height = new_y2 - new_y1
        adj_w = int((new_height-width)/2)
        if x1-adj_w < 0:
            new_x1 = 0
        else:
            new_x1 = x1-adj_w
        if x2+adj_w > img.shape[1]:
            new_x2 = img.shape[1]
        else:
            new_x2 = x2+adj_w
        new_face = img[new_y1:new_y2, new_x1:new_x2]

    sqr_img = cv2.resize(new_face, target_size)
    return sqr_img


y_label_dict = {0: 'Heart', 1: 'Oblong', 2: 'Oval', 3: 'Round', 4: 'Square'}


def predict_face_shape(img_array):
    try:
        face_img = extract_face(img_array)
        new_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        test_img = np.array(new_img, dtype=float)
        test_img = test_img/255
        test_img = np.array(test_img).reshape(1, 224, 224, 3)

        pred = model.predict(test_img)
        label = np.argmax(pred, axis=1)
        shape = y_label_dict[label[0]]
        print(f'Your face shape is {shape}')
        proba = np.max(pred)
        print(f'Probability {np.around(proba*100,2)}')
        return shape
        # run_recommender(shape)
    except Exception as e:
        return({'error': 'Oops!  Something went wrong.  Please try again'})


def predict():
    if 'files' not in request.files:
        resp = jsonify({"msg": "No body files attached in request"})
        resp.status_code = 501
        return resp
    files = request.files['files']
    print(files.filename)
    if files.filename == '':
        resp = jsonify({'msg': "No file image selected"})
        resp.status_code = 505
        return resp

    print(files.filename)
    panjangrambut = request.form['panjang']
    gender = request.form['gender']
    error = {}
    success = False

    if files and allowed_file(files.filename):
        # filename = secure_filename(files.filename)
        # files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_result = cloudinary.uploader.upload(files)
        print(upload_result["secure_url"])
        success = True
    else:
        error[files.filename] = 'File type is not allowed'

    if success and error:
        error['message'] = 'File not uploaded'
        resp = jsonify(error)
        resp.status_code = 500
        return resp
    if success:
        resp = urllib.request.urlopen(upload_result["secure_url"])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print(image)

        faces = detector.detect_faces(image)
        if len(faces) > 0:
            output = predict_face_shape(image)
            suggest = ''
            if output == 'Heart' :
                suggest = "Bentuk Wajah Heart memmiliki area dagu yang lebih lancip dan area dahi yang lebih lebar. Bentuk wajah hati perlu gaya rambut yang bisa membuat keseluruhan wajah terlihat seimbang"
            elif output == 'Oblong' :
                suggest = " Bentuk wajah ini memiliki tulang pipi dan panjang rahang yang cukup spesifik. Garis rahangmu biasanya sejajar dengan tulang pipi."
            elif output == 'Oval' :
                suggest = "Ciri wajah oval memiliki tulang pipi dan dahi yang lebih lebar daripada rahang. Jika berwajah oval, hindari poni karena akan membuat wajahmu bulat."
            elif output == 'Round' :
                suggest = "Bentuk wajah ini banyak ditemui pada orang asia, kamu bisa mencoba Model rambut tipis pada bagian belakang dan samping seperti undercut dapat membuat wajahmu semakin panjang"
            elif output == 'Square' :
                suggest = "Bentuk wajah kotak memiliki rahang yang tegas dan dahi yang lebarnya sejajar dengan rahang"


            rekomen = Recomendations.query.with_entities(Recomendations.id ,Recomendations.image, Recomendations.bentuk, Recomendations.gender, Recomendations.panjangrambut, Recomendations.nama_model, Recomendations.content).filter(
                Recomendations.bentuk == output).filter(Recomendations.panjangrambut == panjangrambut).filter(Recomendations.gender == gender).order_by(Recomendations.nama_model)
            result = rekomen_schema.dump(rekomen)
            return jsonify({
                'status': 200,
                'msg': suggest,
                'Bentuk wajah': output,
                'data': result,
            })
        else :
            return jsonify({
                'status': 200,
                'msg': "Silahkan pilih gambar lain",
                'Bentuk wajah': "Wajah tidak terdeteksi",
                'data': [],
            })
        


def postRecomendations():
    bentuk = request.form['bentuk']
    image = request.form['image']
    gender = request.form['gender']
    panjangrambut = request.form['panjangrambut']
    nama_model = request.form['nama_model']
    content = request.form['content']

    newRecomendations = Recomendations(bentuk, image, gender, panjangrambut, nama_model, content)
    db.session.add(newRecomendations)
    db.session.commit()
    new = rekomens_schema.dump(newRecomendations)
    return jsonify({"msg": "Success post Recomendations", "status": 200, "data": new})


def getAllRecomendation():
    allRecomendation = Recomendations.query.order_by(Recomendations.nama_model).all()
    result = rekomen_schema.dump(allRecomendation)
    return jsonify({"msg": "Success Get all Recomendation", "status": 200, "data": result})


def getRecomendationById(id):
    recomendation = Recomendations.query.get(id)
    detailRecomen = rekomens_schema.dump(recomendation)
    return jsonify({"msg": "Success get detail recomedation", "status": 200, "data": detailRecomen})    