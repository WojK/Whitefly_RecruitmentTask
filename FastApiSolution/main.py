from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.CustomerOpinion import CustomerOpinion
from database import Base, engine, SessionLocal, get_db
from pydantic import BaseModel
from tasks import save_customer_opinion_task

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class CustomerOpinionRequest(BaseModel):
    opinion: str
    name: str


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/async-form", response_class=HTMLResponse)
async def async_form_page(request: Request):
    return templates.TemplateResponse("asyncForm.html", {"request": request})


@app.get("/opinions", response_class=HTMLResponse)
async def opinions_page(request: Request, db: Session = Depends(get_db)):
    opinions = db.query(CustomerOpinion.name, CustomerOpinion.text).order_by(
        CustomerOpinion.created_at.desc()).limit(5).all()

    return templates.TemplateResponse("opinions.html", {"request": request, "opinions": opinions})


@app.post("/opinion")
def create_opinion(name: str = Form(None), opinion: str = Form(...), db: Session = Depends(get_db)):
    if not opinion:
        return RedirectResponse(url="/")

    customer_opinion = CustomerOpinion(text=opinion)
    customer_opinion.name = name if name else "Anonymous"
    db.add(customer_opinion)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/opinion-async")
def create_opinion_async(name: str = Form(None), opinion: str = Form(...), db: Session = Depends(get_db)):
    if not opinion:
        return RedirectResponse(url="/")

    save_customer_opinion_task.delay(opinion, name)

    return RedirectResponse(url="/", status_code=303)
