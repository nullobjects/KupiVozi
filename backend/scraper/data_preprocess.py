import re
from rapidfuzz import process, fuzz
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

MANUFACTURER_COLUMN = "Company"
MODEL_COLUMN = "Model"

def ExtractCarInfo(text):
    car_data = pd.read_csv("./scraper/data/car_data.csv")#, sep=";")

    text = text.lower()

    make_list = car_data[MANUFACTURER_COLUMN].str.strip().str.lower().unique()
    make, make_score, _ = process.extractOne(text, make_list, scorer=fuzz.partial_ratio)
    if make_score < 70:
        make = None

    model = None
    if make:
        model_list = car_data.loc[car_data[MANUFACTURER_COLUMN].str.strip().str.lower() == make.lower(), MODEL_COLUMN].dropna().tolist()
        model, model_score, _ = process.extractOne(text, model_list, scorer=fuzz.partial_ratio)
        if model_score < 70:
            model = None

    year_match = re.search(r"\b(19[0-9]{2}|20[0-2][0-9])\b", text)
    year = year_match.group(0) if year_match else None

    return {"make": make, "model": model, "year": year}


def PreProcessPartsDataForTraining(csv_path="./scraper/data/for_parts.csv", max_tokens=10000, seq_length=30, batch_size=32):
    df = pd.read_csv(csv_path)

    if "Text" not in df.columns or "Label" not in df.columns:
        raise ValueError("The CSV file must contain 'Text' and 'Label' columns.")

    df = df.dropna(subset=["Text", "Label"])

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=max_tokens,
        output_mode='int',
        output_sequence_length=seq_length
    )

    vectorizer.adapt(df["Text"])

    texts = vectorizer(df["Text"]).numpy()
    labels = df["Label"].values

    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    train_dataset = tf.data.Dataset.from_tensor_slices((train_texts, train_labels))
    #test_dataset = tf.data.Dataset.from_tensor_slices((test_texts, test_labels))

    train_dataset = (train_dataset
                     .shuffle(buffer_size=len(train_texts)) 
                     .batch(batch_size)
                     .cache()
                     .prefetch(tf.data.AUTOTUNE))

    #test_dataset = (test_dataset
    #                .batch(batch_size)
    #                .cache()
    #                .prefetch(tf.data.AUTOTUNE))

    return train_dataset, test_texts, test_labels