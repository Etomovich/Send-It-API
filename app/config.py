"""config.py contain configuration files."""
import os


class Config(object):
    """Config."""

    DEBUG = True
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "brian"


class DevelopmentConfig(Config):
    """DevelopmentConfig."""

    DEBUG = True
    TESTING = True
    url = "host='localhost' dbname='data' user='brian' password= 'idfwu8080'"


class TestingConfig(Config):
    """TestingConfig."""

    DEBUG = True
    TESTING = True
    url = "host='localhost' dbname='testdb' user='brian' password='idfwu8080'"


class StagingConfig(Config):
    """StagingConfig."""

    DEBUG = True


class ProductionConfig(Config):
    """ProductionConfig."""

    DEBUG = False
    TESTING = False
    url = "postgres://tuxxcbkoxzmujf:7be0960ab052c84d9896d075b98443e9f4a96eeeca10b73b21c870aa55685ac9@ec2-54-83-8-246.compute-1.amazonaws.com:5432/daeegk5ivabirf"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "production": ProductionConfig
}
