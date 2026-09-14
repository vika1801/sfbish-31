import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/hello", methods=["GET"])
def hello():
    current_time = datetime.utcnow()
    client_ip = request.remote_addr

    new_visit = Visit(visit_time=current_time, ip_address=client_ip)
    db.session.add(new_visit)
    db.session.commit()

    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    