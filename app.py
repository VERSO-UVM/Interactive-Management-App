from flask_app.config import configure_flask_application
from flask import render_template

from flask_app.forms.IndexForm import IndexForm

app = configure_flask_application()


## @author alyssa
@app.route('/', methods=['GET', 'POST'])
def index():

    form: IndexForm = IndexForm()
    message = ''
    return render_template('index.html', form=form, message=message)


# Alyssa
# You should only run app.py directly for development.
# It should be run through wsgi.py gateway otherwise
if __name__ == "__main__":
    app.run(host='0.0.0.0')
