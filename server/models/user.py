import os
from datetime import datetime, timedelta, timezone

import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from server import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def register(data):
        """Register a new user."""
        try:
            hashed_password = generate_password_hash(
                data["password"], method="pbkdf2:sha256"
            )
            new_user = User(email=data["email"], password=hashed_password)
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
            encoding_key = os.getenv("SECRET_KEY", "dev")
            token = jwt.encode(
                {
                    "id": user.id,
                    "exp": datetime.now() + timedelta(hours=1),
                },
                key=encoding_key,
                algorithm="HS256",
            )
            return token
        return None
