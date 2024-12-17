# Here i created an NLP classifier to classify if a car auction
# is for damaged or for parts, we can ignore these detected auctions
# or even create a section where people specifically want these kind of auctions
import tensorflow as tf
from tensorflow.keras.optimizers import Adam

def DamagedOrForPartsModel():
    model = tf.keras.Sequential([
        tf.keras.layers.Input((120,)),
        tf.keras.layers.Embedding(10000, 9),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        loss="binary_crossentropy",
        optimizer=Adam(learning_rate = 0.001),
        metrics=["accuracy"]
    )

    return model