from flask_app.config import configure_flask_application

app = configure_flask_application()


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
