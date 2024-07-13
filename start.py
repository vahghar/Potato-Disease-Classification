from fastapi import FastAPI,File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os
from fastapi.middleware.cors import CORSMiddleware

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
app = FastAPI() #instance of fastapi


ORIGINS = [
    "https://localhost",
    "https://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials = True,
    allow_methods="*",
    allow_headers="*",
    
)
 
MODEL = tf.keras.models.load_model("C:/Users/Pushpa_Rawat/OneDrive/Desktop/Potato_Dis/saved_models/1.keras")
CLASS_NAMES =["Early Blight","Late Blight","Healthy"]

@app.get("/ping")
async def ping():
    return "hello, i am alive"

def read_file_as_image(data)-> np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)
    prediction = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    return {
        'class':predicted_class,
        'confidence':float(confidence)
    }
    

if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8000)