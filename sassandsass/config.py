class Config:
    DATABASE = '/tmp/sassandsass.db'
    SECRET_KEY = 'cream'
    LANDING_PAGE = 'aboutus'
    DEBUG = False
    STYLES = ["structure.css", "content.css", "nav.css" ]
    SCRIPTS = ["jquery-1.10.2.min.js","jquery.nav.js"]
    
class DebugConfig(Config):
    DEBUG = True
