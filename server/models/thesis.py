from ..app import DB

class Thesis(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(120), nullable=False)
    content = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return f"<Thesis {self.title}>"
