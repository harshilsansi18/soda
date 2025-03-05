from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from backend.routes.upload import router as upload_router
from backend.routes.validations import router as validation_router

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="frontend/templates")

# Include API routes
app.include_router(upload_router, prefix="/api")
app.include_router(validation_router, prefix="/api/validations")

# Serve frontend pages
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/validation")
async def validation_page(request: Request):
    return templates.TemplateResponse("validation.html", {"request": request})
