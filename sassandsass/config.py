import os.path

class Config:
    DATABASE = '/tmp/sassandsass.db'
    SECRET_KEY = '\x15\x1b\xc9\x9b$\xcdX\xf1\xafK\xb58RL\xe5\x92<\x11\x8ej~\t\x03\xcb'
    LANDING_PAGE = 'aboutus'
    DEBUG = False
    STYLES = ["structure.css", "content.css", "nav.css", "edit_forms.css"]
    SCRIPTS = ["jquery-1.10.2.min.js",
            "jquery.nav.js",
            "edit_form_loader.js"]
    MEDIA_ICONS = {"Twitter": "https://twitter.com/sassandsass",
            "LinkedIn": "https://www.linkedin.com/company/3269338?trk=tyah"}
    IMAGE_FOLDER = os.path.abspath("sassandsass/static/img")
    CONSUMER_KEY = '5GAdCxJZbjUvPqa24rWGZCSUSAoow2MtZrEj1uBipKiZhNAZ4W'
    CONSUMER_SECRET = 'jf0rnwdWfopxlkbAcN4q7iaJxOYovKqZ867ehmSe42cLDfG2jS'
    
class DebugConfig(Config):
    DEBUG = True
