from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class tourist_route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return '<tourist_route {} {}>'.format(self.published, self.url)