import os

''''class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True'''
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'postgresql://flask_db_c5i2_user:OkRsv9pUzQszU2mvqn8TllKfYVdIZzLT@dpg-ctnfjibqf0us73agck7g-a.oregon-postgres.render.com:5432/flask_db_c5i2', 'sqlite:///default.db')  # Default to SQLite for local testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
