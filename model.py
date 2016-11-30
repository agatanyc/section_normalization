from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Manifest(db.Model):

    __tablename__ = 'manifest'

    primary_key = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # section_id,section_name,row_id,row_name
    section_id = db.Column(db.Integer())
    section_name = db.Column(db.Integer())
    row_id = db.Column(db.Integer())
    row_name = db.Column(db.String(40))

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    init_db(app)
    db.create_all()

    print "Connected to DB"