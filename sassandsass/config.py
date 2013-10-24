class Config:
    DATABASE = '/tmp/sassandsass.db'
    SECRET_KEY = 'cream'
    LANDING_PAGE = 'aboutus'
    DEBUG = False
    STYLES = ["structure.css", "content.css", "nav.css" ]
    SCRIPTS = ["jquery-1.10.2.min.js","jquery.nav.js",'edit_form_loader.js']
    MEDIA_ICONS = {"Twitter": "https://twitter.com/sassandsass",
            "LinkedIn": "https://www.linkedin.com/company/3269338?trk=tyah"}
    
class DebugConfig(Config):
    DEBUG = True
