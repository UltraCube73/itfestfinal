from flask_sqlalchemy import SQLAlchemy
from application import app
addr_file = open('sqladdr', 'r')
app.config['SQLALCHEMY_DATABASE_URI'] = addr_file.read()
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(40), unique=False, nullable=False)
    user_func = db.Column(db.String(20), unique=False, nullable=True)
    user_was_shown = db.Column(db.Boolean, default=False, nullable=False)
    user_attempts = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username