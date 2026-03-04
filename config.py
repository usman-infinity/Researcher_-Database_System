import os


class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///research.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False