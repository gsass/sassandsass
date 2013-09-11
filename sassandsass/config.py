class Config:
    DATABASE = '/tmp/sassandsass.db'
    SECRET_KEY = 'cream'
    LANDING_PAGE = 'aboutus'
    DEBUG = False
    
class DebugConfig(Config):
    DEBUG = True
