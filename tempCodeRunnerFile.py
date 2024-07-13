
    CORSMiddleware,
    allow_origins=origins,
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