# this code sets up a User model for a Flask application using SQLAlchemy. The User model has fields for id, email, and password, and it generates a unique identifier for each user. This is the foundation for working with user data in a Flask application and storing it in a database.

from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import pickle
import pandas as pd
import numpy as np
from flask_login import UserMixin
db = SQLAlchemy()




  
def get_uuid():
    return uuid4().hex

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.String(345), nullable=False)
