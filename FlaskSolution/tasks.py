from celery import shared_task
from init import db, flask_app, celery_app
from models.CustomerOpinion import CustomerOpinion


@shared_task(ignore_result=False)
def save_customer_opinion_task(opinion, name):
    customer_opinion = CustomerOpinion(text=opinion)
    customer_opinion.name = name if name else "Anonymous"
    db.session.add(customer_opinion)
    db.session.commit()
