from flask import Flask
from backend.views import views

app = Flask(__name__, template_folder="frontend/templates")
# secret key
app.config["SECRET_KEY"] = "c983hdjkos93yfh287chj32947gsjcyf"

# register routes blueprints
app.register_blueprint(views, url_prefix="/")


if __name__ == '__main__':
    app.run()
