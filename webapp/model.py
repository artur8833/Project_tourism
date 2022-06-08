from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
SQLALCHEMY_TRACK_MODIFICATIONS = False


class routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    Description = db.Column(db.String(120), nullable=False)

    @property
    def __repr__(self):
        return "<routes {} {}>".format(self.title, self.Description)
