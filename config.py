import os
#from datetime import timedelta

''''class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True'''
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',  # Use the 'DATABASE_URL' environment variable
        # 'postgresql://flask_db_c5i2_user:OkRsv9pUzQszU2mvqn8TllKfYVdIZzLT@dpg-ctnfjibqf0us73agck7g-a.oregon-postgres.render.com:5432/flask_db_c5i2'
        'postgresql://server:V9I#%j{+S^JG"e`_@35.185.232.38:5432/ConfigNew'  # Default to this if DATABASE_URL is not set
    ).replace("postgres://", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
    #JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '3df667c052b722636ad97ec98da93a272091a0cdb3e18fa448112e04d3f7ae43')  
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)  

    # app.config["SQLALCHEMY_DATABASE_URI"] = (
    #     db_url or 'postgresql://server:V9I#%j{+S^JG"e`_@35.185.232.38:5432/ConfigNew'
    # )
    # app.config["SQLALCHEMY_BINDS"] = {
    #     "ZIGS": 'postgresql://server:V9I#%j{+S^JG"e`_@35.185.232.38:5432/ZIGS'
    # }
