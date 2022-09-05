class Config:
    SECRET_KEY = "123!qwe"

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'sirf'

config={
    'development': DevelopmentConfig
}