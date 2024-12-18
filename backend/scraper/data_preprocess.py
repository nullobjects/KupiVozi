import re
from rapidfuzz import process, fuzz
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

MANUFACTURER_COLUMN = "Company"
MODEL_COLUMN = "Model"

def ExtractCarInfo(text):
    car_data = pd.read_csv("./scraper/data/car_data.csv")  # Load car data

    text = text.lower()

    # Manufacturer
    make_list = car_data[MANUFACTURER_COLUMN].str.strip().str.lower().unique()
    make, make_score, _ = process.extractOne(text, make_list, scorer=fuzz.partial_ratio)
    if make_score < 70:
        make = None

    # Model
    model = None
    if make:
        model_list = car_data.loc[car_data[MANUFACTURER_COLUMN].str.strip().str.lower() == make.lower(), MODEL_COLUMN].dropna().tolist()
        model, model_score, _ = process.extractOne(text, model_list, scorer=fuzz.partial_ratio)
        if model_score < 70:
            model = None

    # Year
    year_match = re.search(r"(^|\D)(\d{4})(?=\D|$)", text)
    year = year_match.group(0) if year_match else None
    year = year.strip()

    # Price
    price_data = ExtractPriceAndCurrency(text)

    # Kilometers
    km_match = re.search(r"(?<!\d)(\d{1,3}(?:\s*\d{3})?)\s*[-–]\s*(\d{1,3}(?:\s*\d{3})?)", text)
    kilometers = None
    if km_match:
        kilometers = f"{km_match.group(1).replace(' ', '')}-{km_match.group(2).replace(' ', '')}"

    return {
        "make": make,
        "model": model,
        "year": year,
        "price": price_data,
        "kilometers": kilometers,
    }

def ExtractPriceAndCurrency(text):
    match = re.search(
        r"(\b\d{1,3}(?:[\s,]?\d{3})*(?:\.\d{1,2})?)\s*(€|eur|usd|ден|еур|\$|mkd|мкд)|"  # Price followed by currency
        r"(€|eur|usd|ден|еур|\$|mkd|мкд)\s*(\b\d{1,3}(?:[\s,]?\d{3})*(?:\.\d{1,2})?)",  # Currency followed by price
        text,
        re.IGNORECASE,
    )
    if match:
        if match.group(1):
            price = match.group(1).replace(" ", "").replace(",", "")
            currency = match.group(2).upper()
        elif match.group(4):
            price = match.group(4).replace(" ", "").replace(",", "")
            currency = match.group(3).upper()
        else:
            price, currency = None, "UNKNOWN"

        return price + currency
    return None


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

def IsCarValid(CarData):
    return not (CarData["make"] == None or CarData["model"] == None or CarData["year"] == None or CarData["price"] == None or CarData["link"] == None)