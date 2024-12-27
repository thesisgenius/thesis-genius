from server import db


class Thesis(db.Model):
    __tablename__ = "theses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="In Progress")
    submission_date = db.Column(db.Date, nullable=True)
