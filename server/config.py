class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://user@localhost/db'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@prod/db'

