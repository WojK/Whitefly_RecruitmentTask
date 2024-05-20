from flask import render_template, request, url_for, flash, redirect
from sqlalchemy import desc

from init import db, flask_app
from models.CustomerOpinion import CustomerOpinion
from tasks import save_customer_opinion_task


@flask_app.route("/")
def homepage():
    return render_template('index.html')


@flask_app.route("/form", methods=('GET', 'POST'))
def form_page():
    if request.method == 'POST':
        opinion = request.form['opinion']
        name = request.form['name']
        if not opinion:
            flash('Your opinion must have at least one character!')
        else:
            customer_opinion = CustomerOpinion(text=opinion)
            customer_opinion.name = name if name else "Anonymous"
            db.session.add(customer_opinion)
            db.session.commit()
            return redirect(url_for('homepage'))
    return render_template('form.html')


@flask_app.route("/async-form", methods=('GET', 'POST'))
def async_form_page():
    if request.method == 'POST':
        opinion = request.form['opinion']
        name = request.form['name']
        if not opinion:
            flash('Your opinion must have at least one character!')
        else:
            save_customer_opinion_task.delay(opinion, name)
            return redirect(url_for('homepage'))
    return render_template('asyncForm.html')

@flask_app.route("/opinions")
def opinions_page():
    opinions = (CustomerOpinion.query.with_entities(CustomerOpinion.name, CustomerOpinion.text).
                order_by(desc(CustomerOpinion.created_at)).limit(5).all())

    print(opinions)
    return render_template('opinions.html', opinions=opinions)


if __name__ == "__main__":
    flask_app.run(debug=True)
