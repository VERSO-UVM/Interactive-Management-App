from flask_app.config import configure_flask_application
from flask import render_template

from flask_app.forms.IndexForm import IndexForm
from flask_app.forms.WorkshopForm import WorkshopForm

app = configure_flask_application()


## @author alyssa
@app.route('/', methods=['GET', 'POST'])
def index():

    form: IndexForm = IndexForm()
    message = ''
    return render_template('index.html', form=form, message=message)

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
