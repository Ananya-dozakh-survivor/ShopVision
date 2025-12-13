from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import tensorflow as tf
import io
import base64
import json
from tensorflow.keras.applications.efficientnet import preprocess_input
import uvicorn

# ------------------------------
# Load Class Names (76 classes)
# ------------------------------
with open("class_names.json", "r") as f:
    class_names = json.load(f)

print("Loaded classes:", len(class_names))

# ------------------------------
# Load Model
# ------------------------------
MODEL_PATH = "fruit_model1.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded!")

# ------------------------------
# Price Table
# ------------------------------
price_table = {
    "Apple": 50, "Apricot": 120, "Avocado": 140, "Banana": 30, "Beans": 40,
    "Beetroot": 35, "Blackberrie": 160, "Blueberry": 180, "Cabbage": 25,
    "Cactus": 60, "Cantaloupe": 70, "Carrot": 35, "Cashew": 300, "Cauliflower": 40,
    "Cherimoya": 150, "Cherry": 140, "Chestnut": 200, "Clementine": 80,
    "Cocos": 50, "Corn": 30, "Cucumber": 25, "Dates": 220, "Eggplant": 40,
    "Fig": 120, "Ginger": 90, "Gooseberry": 70, "Granadilla": 160, "Grape": 90,
    "Grapefruit": 80, "Guava": 50, "Hazelnut": 240, "Huckleberry": 170,
    "Kaki": 110, "Kiwi": 90, "Kohlrabi": 30, "Kumquats": 140, "Lemon": 60,
    "Limes": 40, "Lychee": 180, "Mandarine": 70, "Mango": 120,
    "Mangostan": 200, "Melon": 80, "Mulberry": 130, "Nectarine": 90,
    "Nut": 250, "Onion": 25, "Orange": 60, "Papaya": 80, "Passion": 160,
    "Passionfruit": 160, "Peach": 90, "Pear": 70, "Pepino": 110,
    "Pepper": 60, "Physalis": 150, "Pineapple": 100, "Pistachio": 280,
    "Pitahaya": 200, "Plum": 90, "Pomegranate": 120, "Pomelo": 70,
    "Potato": 20, "Quince": 70, "Rambutan": 200, "Raspberry": 180,
    "Redcurrant": 140, "Salak": 180, "Starfruit": 120, "Strawberry": 150,
    "Tamarillo": 180, "Tangelo": 100, "Tomato": 40, "Walnut": 260,
    "Watermelon": 50, "Zucchini": 30
}

# ------------------------------
# FastAPI Setup
# ------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Preprocessing for EfficientNet
# ------------------------------


def prepare_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))          # NEW CORRECT SIZE
    img = np.array(image)
    img = preprocess_input(img)               # EfficientNet normalization
    img = np.expand_dims(img, axis=0)
    return img

# ------------------------------
# Prediction Logic
# ------------------------------


def predict_image(image: Image.Image):
    x = prepare_image(image)
    preds = model.predict(x)[0]
    idx = int(np.argmax(preds))

    cls = class_names[idx]
    confidence = float(preds[idx])
    price = price_table.get(cls, "N/A")

    return cls, confidence, price

# ------------------------------
# /predict — Image Upload
# ------------------------------


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))
    except:
        return JSONResponse({"error": "Invalid image"}, status_code=400)

    cls, conf, price = predict_image(image)

    return {
        "class": cls,
        "confidence": round(conf * 100, 2),
        "price": price
    }

# ------------------------------
# /predict_camera — Base64 Snapshot
# ------------------------------


@app.post("/predict_camera")
async def predict_camera(data: dict):
    try:
        img_b64 = data.get("image")
        img_bytes = base64.b64decode(img_b64.split(",")[1])
        image = Image.open(io.BytesIO(img_bytes))
    except:
        return JSONResponse({"error": "Invalid base64 image"}, status_code=400)

    cls, conf, price = predict_image(image)

    return {
        "class": cls,
        "confidence": round(conf * 100, 2),
        "price": price
    }

# ------------------------------
# Static Images
# ------------------------------


@app.get("/confusion")
async def get_confusion():
    return FileResponse("confusion_matrix1.png")


@app.get("/gallery")
async def get_gallery():
    return FileResponse("sample_gallery.png")

# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
