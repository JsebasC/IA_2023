from flask import Flask, request, jsonify, make_response
import json
from flask_cors import CORS
import base64
import io
import numpy as np 
from PIL import Image
from tensorflow import keras 
import keras.utils as image
import tensorflow as tf
import numpy as np
import os
import mysql.connector

# Configurar la conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flowerclassification"
)

mycursor = mydb.cursor()

app = Flask(__name__)
CORS(app)
model_filename = "flower-classification.h5"
model = keras.models.load_model(model_filename)
CLASSES = ['pink primrose',    'hard-leaved pocket orchid', 'canterbury bells', 'sweet pea',     'wild geranium',     'tiger lily',           'moon orchid',              'bird of paradise', 'monkshood',        'globe thistle',         # 00 - 09
     'snapdragon',       "colt's foot",               'king protea',      'spear thistle', 'yellow iris',       'globe-flower',         'purple coneflower',        'peruvian lily',    'balloon flower',   'giant white arum lily', # 10 - 19
     'fire lily',        'pincushion flower',         'fritillary',       'red ginger',    'grape hyacinth',    'corn poppy',           'prince of wales feathers', 'stemless gentian', 'artichoke',        'sweet william',         # 20 - 29
     'carnation',        'garden phlox',              'love in the mist', 'cosmos',        'alpine sea holly',  'ruby-lipped cattleya', 'cape flower',              'great masterwort', 'siam tulip',       'lenten rose',           # 30 - 39
     'barberton daisy',  'daffodil',                  'sword lily',       'poinsettia',    'bolero deep blue',  'wallflower',           'marigold',                 'buttercup',        'daisy',            'common dandelion',      # 40 - 49
     'petunia',          'wild pansy',                'primula',          'sunflower',     'lilac hibiscus',    'bishop of llandaff',   'gaura',                    'geranium',         'orange dahlia',    'pink-yellow dahlia',    # 50 - 59
     'cautleya spicata', 'japanese anemone',          'black-eyed susan', 'silverbush',    'californian poppy', 'osteospermum',         'spring crocus',            'iris',             'windflower',       'tree poppy',            # 60 - 69
     'gazania',          'azalea',                    'water lily',       'rose',          'thorn apple',       'morning glory',        'passion flower',           'lotus',            'toad lily',        'anthurium',             # 70 - 79
     'frangipani',       'clematis',                  'hibiscus',         'columbine',     'desert-rose',       'tree mallow',          'magnolia',                 'cyclamen ',        'watercress',       'canna lily',            # 80 - 89
     'hippeastrum ',     'bee balm',                  'pink quill',       'foxglove',      'bougainvillea',     'camellia',             'mallow',                   'mexican petunia',  'bromelia',         'blanket flower',        # 90 - 99
     'trumpet creeper',  'blackberry lily',           'common tulip',     'wild rose']
  
def baseJPG(imgstring):
    imgdata = base64.b64decode(imgstring)
        
    path = "images/"+imgstring
    
    file1 = request.files['file1']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
       
    print(filename)
    with open(filename, 'wb') as f:
        f.write(imgdata)
  
    return ""

@app.route('/predict', methods=["POST"])
def predict_multipart():
    try:
        # Verificar si hay un archivo en la solicitud
        if 'imageUpload' not in request.files:
            return jsonify({"error": "No se encontró ninguna imagen"})

        # Obtener el archivo de imagen desde la solicitud
        uploaded_file = request.files['imageUpload']

        # Guardar el archivo de imagen en el servidor
        if uploaded_file.filename != '':
            file_path = os.path.join("images", uploaded_file.filename)
            
            uploaded_file.save(file_path)
       
    
            # Cargar la imagen
            img = tf.io.read_file(file_path)
            img = tf.image.decode_image(img, channels=3)  # Decodificar la imagen
     
            # Redimensionar la imagen a 224x224
            img = tf.image.resize(img, [224, 224])
     
            # Convertir la imagen a tipo float32 en el rango [0, 1]
            img = tf.image.convert_image_dtype(img, tf.float32)
     
            # Expandir las dimensiones para tener el formato (1, 224, 224, 3)
            img = tf.expand_dims(img, 0)
     
            # Realizar la predicción en la imagen
            probabilities = model.predict(img)
            predicted_class_index = np.argmax(probabilities, axis=-1)
            predicted_class_name = CLASSES[predicted_class_index[0]]
        
            # Obtener la probabilidad máxima predicha
            max_probability = np.max(probabilities)
            
            # Establecer un umbral
            umbral_confianza = 0.99  # Por ejemplo, un umbral del 80%
            message = ""
            clase = ""
            # Comprobar si la probabilidad máxima está por debajo del umbral
            if max_probability < umbral_confianza:
                clase = "sin clasificar"
                message = "La imagen no se relaciona con las clases establecidas."
            else:
                clase = predicted_class_name
                message = f"Clase predicha: {clase}"
                
            Save_Image(uploaded_file.filename, clase)
            return jsonify({"Message": message})
        else:
            return jsonify({"error": "No se recibió un archivo de imagen válido"})

    except Exception as e:
        return jsonify({"error": str(e)})

    
def Save_Image(photoName, predictedClass):
    try:    
        # Insertar datos en la tabla 'imagenes'
        sql = "INSERT INTO images (Photo, Class) VALUES (%s, %s)"
        val = (photoName, predictedClass)
        
        mycursor.execute(sql, val)
        mydb.commit()

        return jsonify({"message": "Datos guardados exitosamente en la base de datos"})
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/ping', methods=["GET"])
def show_form_data():
    
    return jsonify({"state":"ok"})

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8080)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Configuración para permitir todos los orígenes
    app.run(host="0.0.0.0")
