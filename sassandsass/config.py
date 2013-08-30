class Config:
    DATABASE = '/tmp/flaskr.db'
    SECRET_KEY = 'cream'
    
class DebugConfig(Config):
    DEBUG = True
