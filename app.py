from flask_app.config import configure_flask_application
from flask import Flask, render_template, request, redirect, url_for
import uuid
from datetime import datetime

from flask_app.forms.IndexForm import IndexForm
from flask_app.forms.WorkshopForm import WorkshopForm

app = configure_flask_application()


## @author alyssa
@app.route('/', methods=['GET', 'POST'])
def index():

    form: IndexForm = IndexForm()
    message = ''
    return render_template('index.html', form=form, message=message)
    return render_template('index.html', factors=factors, categories=categories)

## author tushar
factors = []
categories = []

class Factor:
    def __init__(self, idea, clarification, label, category):
        self.id = str(uuid.uuid4())
        self.idea = idea
        self.clarification = clarification
        self.label = label
        self.category = category
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

class Category:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


@app.route('/add_factor', methods=['POST'])
def add_factor():

    if request.method == 'POST':
        idea = request.form['idea']
        clarification = request.form['clarification']
        label = request.form['label']
        category = request.form['category']
        reason = request.form['reason']

        new_factor = Factor(idea=idea, clarification=clarification, label=label, category=category)
        factors.append(new_factor)

    return redirect(url_for('index'))


@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    factor = next((f for f in factors if f.id == id), None)
    if factor is None:
        return "Factor not found", 404

    if request.method == 'POST':
        factor.idea = request.form['idea']
        factor.clarification = request.form['clarification']
        factor.label = request.form['label']
        factor.category = request.form['category']
        factor.updated_at = datetime.utcnow()

        return redirect(url_for('index'))

    return render_template('edit_factor.html', factor=factor, categories=categories)

@app.route('/delete_factor/<id>')
def delete_factor(id):
    global factors
    factors = [f for f in factors if f.id != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# @author grace
@app.route('/workshop', methods=['GET', 'POST'])
def workshop():

    form: WorkshopForm = WorkshopForm()

    if form.validate_on_submit():
        print("VALID")

        data = {'trigger_question': form.trigger_field.data,
                'context_statement': form.context_statement.data,
                'title': form.title.data,
                'date': form.date.data,
                'host_organization': form.host_organization.data,
                'location': form.location.data,
                'objectives': form.objectives.data
                }
        print(data)

    message = ''
    return render_template('workshop.html', form=form, message=message)


# Alyssa
# You should only run app.py directly for development.
# It should be run through wsgi.py gateway otherwise
if __name__ == "__main__":
    app.run(host='0.0.0.0')



