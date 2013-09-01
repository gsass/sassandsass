class Config:
    DATABASE = '/tmp/flaskr.db'
    SECRET_KEY = 'cream'
    LANDING_PAGE = 'aboutus'
    
class DebugConfig(Config):
    DEBUG = True
