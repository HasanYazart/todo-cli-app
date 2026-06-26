from flask import Flask
from models import db
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app = Flask(__name__)
app.secret_key = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
