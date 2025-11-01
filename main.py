from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from rembg import remove, new_session
from PIL import Image
import base64
import io

app = FastAPI()
session = new_session("isnet-general-use")

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        output = remove(image_bytes, session=session)

        buffer = io.BytesIO()
        Image.open(io.BytesIO(output)).save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode()

        return JSONResponse({"image": encoded})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
