from flask_app.config import configure_flask_application
from flask import render_template

app = configure_flask_application()


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
