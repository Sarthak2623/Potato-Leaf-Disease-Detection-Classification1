"""
FastAPI Server for Potato Leaf Disease Detection and Classification.
Provides RESTful APIs for image diagnosis, sample management, and serves the Web UI.
"""

import os
import io
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image

from ml.classifier import predict_leaf_disease, load_image
from ml.disease_info import DISEASE_CLASSES, DISEASE_DETAILS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
SAMPLES_DIR = os.path.join(STATIC_DIR, "samples")

app = FastAPI(
    title="potatoGuardProject — Potato Leaf Disease Detection API",
    description="Machine Learning system for detecting Early Blight, Late Blight, and Healthy potato leaves",
    version="1.0.0"
)

# Mount static directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Serve the modern interactive Single Page Application."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "classes": DISEASE_CLASSES,
            "details": DISEASE_DETAILS
        }
    )


@app.get("/favicon.ico")
async def favicon():
    """Return 204 No Content for browser favicon requests."""
    from starlette.responses import Response
    return Response(status_code=204)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Potato Leaf Disease Classifier",
        "supported_classes": DISEASE_CLASSES
    }


@app.get("/api/samples")
async def list_sample_images():
    """Return available sample leaf images for instant 1-click testing."""
    samples = [
        {
            "id": "early_blight",
            "name": "Early Blight (Alternaria solani)",
            "expected_class": "Potato___Early_blight",
            "filename": "early_blight_sample.jpg",
            "url": "/static/samples/early_blight_sample.jpg",
            "description": "Notice target-like concentric rings and chlorotic halos."
        },
        {
            "id": "late_blight",
            "name": "Late Blight (Phytophthora infestans)",
            "expected_class": "Potato___Late_blight",
            "filename": "late_blight_sample.jpg",
            "url": "/static/samples/late_blight_sample.jpg",
            "description": "Notice water-soaked purplish dark lesions on margins."
        },
        {
            "id": "healthy",
            "name": "Healthy Foliage (Solanum tuberosum)",
            "expected_class": "Potato___healthy",
            "filename": "healthy_sample.jpg",
            "url": "/static/samples/healthy_sample.jpg",
            "description": "Vibrant emerald green leaf with uniform coloration."
        }
    ]
    return {"samples": samples}


@app.get("/api/disease-info")
async def get_disease_encyclopedia():
    """Return complete clinical and agronomic encyclopedia metadata."""
    return {
        "classes": DISEASE_CLASSES,
        "details": DISEASE_DETAILS
    }


@app.post("/api/predict")
async def predict_image(request: Request):
    """
    Classify a potato leaf image and return pathology diagnosis,
    confidence metrics, severity score, and visual heatmaps.
    Accepts:
    1. Form file upload ('file')
    2. Base64 encoded image ('image_base64')
    3. Sample ID ('sample_id')
    4. JSON payload with image_base64 or sample_id
    """
    try:
        pil_img = None
        content_type = request.headers.get("content-type", "")

        file_obj = None
        image_base64 = None
        sample_id = None

        if "application/json" in content_type:
            body = await request.json()
            image_base64 = body.get("image_base64")
            sample_id = body.get("sample_id")
        else:
            form = await request.form()
            file_obj = form.get("file")
            image_base64 = form.get("image_base64")
            sample_id = form.get("sample_id")

        # 1. Try file object if uploaded
        if file_obj is not None and hasattr(file_obj, "read"):
            filename = getattr(file_obj, "filename", None)
            if filename:
                content = await file_obj.read()
                if content and len(content) > 0:
                    pil_img = load_image(content)

        # 2. Try image_base64 if file wasn't loaded
        if pil_img is None and isinstance(image_base64, str) and image_base64.strip():
            raw_b64 = image_base64.strip()
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            if raw_b64:
                img_bytes = base64.b64decode(raw_b64)
                pil_img = load_image(img_bytes)

        # 3. Try sample_id if neither was provided
        if pil_img is None and isinstance(sample_id, str) and sample_id.strip():
            sid = sample_id.strip()
            sample_map = {
                "early_blight": "early_blight_sample.jpg",
                "late_blight": "late_blight_sample.jpg",
                "healthy": "healthy_sample.jpg"
            }
            if sid in sample_map:
                sample_path = os.path.join(SAMPLES_DIR, sample_map[sid])
                if os.path.exists(sample_path):
                    pil_img = load_image(sample_path)

        if pil_img is None:
            raise HTTPException(
                status_code=400,
                detail="No image provided. Please upload a file, webcam capture, or select a sample."
            )

        # Run ML Diagnostic Classifier
        results = predict_leaf_disease(pil_img)
        return JSONResponse(content={"success": True, "data": results})

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
