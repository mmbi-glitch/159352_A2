from os import path

from flask import Flask

from flask_login import LoginManager

from backend.views import views
from database import db, DB_NAME
from database.models import Customer, flights

login_manager = LoginManager()
login_manager.login_view = "views.manage"

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
# secret key
app.config["SECRET_KEY"] = "c983hdjkos93yfh287chj32947gsjcyf"
# where database will be created
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../database/{DB_NAME}"

# register routes blueprints
app.register_blueprint(views, url_prefix="/")

# initialize database

with app.app_context():
    db.init_app(app=app)

    if not path.exists(f"database/{DB_NAME}"):
        db.create_all()
        db.session.add_all(flights)
        db.session.commit()
        print("Created SQLite database!")
    else:
        print("SQLite database exists!")

    login_manager.init_app(app)


    # tells flask how to load a user
    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    # print(Flight.query.all())

if __name__ == '__main__':
    app.run()
