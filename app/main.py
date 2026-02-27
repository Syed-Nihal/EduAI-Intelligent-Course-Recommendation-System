from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import create_tables
from app.routes.students import router as student_router

app = FastAPI()

# Create DB tables
create_tables()

# Include student routes
app.include_router(student_router)

# Setup templates
templates = Jinja2Templates(directory="app/templates")


# Home Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})