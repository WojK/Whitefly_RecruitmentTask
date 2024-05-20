from celery import Celery
from sqlalchemy.orm import Session

from database import SessionLocal
from models.CustomerOpinion import CustomerOpinion

celery_app = Celery(__name__, broker="redis://localhost:6379", backend="redis://localhost:6379")


@celery_app.task()
def save_customer_opinion_task(opinion, name):
    db: Session = SessionLocal()
    
    try:
        customer_opinion = CustomerOpinion(text=opinion)
        customer_opinion.name = name if name else "Anonymous"
        db.add(customer_opinion)
        db.commit()
    finally:
        db.close()
