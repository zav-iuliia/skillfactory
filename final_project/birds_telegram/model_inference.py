import json

import numpy as np
from PIL import Image

CLASS_COUNT = 78
HEIGHT = 224
WIDTH = 224
IMG_SHAPE = (HEIGHT, WIDTH, 3)
IMG_SIZE = (HEIGHT, WIDTH)


def create_model():
    from tensorflow import keras
    from tensorflow.keras import regularizers
    from tensorflow.keras.layers import BatchNormalization, Dense, Dropout
    from tensorflow.keras.models import Model, Sequential, load_model
    from tensorflow.keras.optimizers import Adam, Adamax

    base_model = keras.applications.EfficientNetB1(
        include_top=False, weights="imagenet", input_shape=IMG_SHAPE, pooling="max"
    )
    x = base_model.output
    x = keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001)(x)
    x = Dense(
        256,
        kernel_regularizer=regularizers.l2(l=0.016),
        activity_regularizer=regularizers.l1(0.006),
        bias_regularizer=regularizers.l1(0.006),
        activation="relu",
    )(x)
    x = Dropout(rate=0.45, seed=123)(x)
    output = Dense(CLASS_COUNT, activation="softmax")(x)
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(
        Adamax(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"]
    )
    model.load_weights("model.h5")
    return model


def load_lookup_map():
    return {int(k): v for k, v in json.load(open("lookup_map.json")).items()}


def preprocess_photo(photo_obj):
    img = Image.open(photo_obj)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(IMG_SIZE)
    return np.expand_dims(np.asarray(img), axis=0)


def predict_species(photo_obj):
    model = create_model()
    lookup_map = load_lookup_map()

    pred = model.predict(preprocess_photo(photo_obj))
    best_pred = pred.argmax()
    best_score = round(pred[0][best_pred] * 100, 1)
    species = lookup_map[best_pred]
    if best_score < 50:
        return "No such bird in our database"
    return f"Best prediction: {species} ({best_score}%)"
