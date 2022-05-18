import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Create a Congiguration class
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '587')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
                                  ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SMS_MAIL_SUBJECT_PREFIX = '[DRE School Management System]'
    SMS_MAIL_SENDER = 'DRE-SMS <dresms@email.com>'
    SMS_ADMIN = os.environ.get('SMS_ADMIN')
    
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass
    
#Define the type of configuration for the app(Testing, Development, and Production)
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'mysql+pymysql://root:newpasssql@localhost/dre-sms'
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
#Create config dictionary for the defined classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}
    