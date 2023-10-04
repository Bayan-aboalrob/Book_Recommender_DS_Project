
from app import db,app
from models import User

# 254,   2276,   2766,   2977,   3363,   3757,   4017,   4385,


def seed_data():
    sample_data = [
        {"user_id": 254, "email": "refqi@gmail.com", "password": "refqi2023"},
        {"user_id": 2276, "email": "marwan@gmail.com", "password": "marwan2023"},
        {"user_id": 2766, "email": "firas@gmail.com", "password": "firas2023"},
        {"user_id": 2977, "email": "sameeh@gmail.com", "password": "sameeh2023"},
        {"user_id": 3363, "email": "zayn@gmail.com", "password": "zayn2023"},
    ]
    with app.app_context():
        for data in sample_data:
            user = User(
                user_id=data["user_id"],
                email=data["email"],
                password=data["password"]
            )
            db.session.add(user)

        db.session.commit()
