import jwt
from server.app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def register(data):
        """Register a new user."""
        try:
            hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
            new_user = User(email=data['email'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            print(f"Error registering user: {e}")
            return None

    @staticmethod
    def login(email, password):
        """Login a user and return a JWT token if successful."""
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            token = jwt.encode(
                {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                current_app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            return token
        return None