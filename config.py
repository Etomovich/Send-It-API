"""config.py contains configuration files."""
import os


class Config(object):
    """Config."""

    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "brian"


class DevelopmentConfig(Config):
    """DevelopmentConfig."""

    DEBUG = True
    TESTING = True
    DATABASE_URL = "host='localhost' port='5432' dbname='data' user='brian'"


class TestingConfig(Config):
    """TestingConfig."""

    DEBUG = True
    TESTING = True
    DATABASE_URL = "host='localhost' port='5432' dbname='testdb' user='brian'"


class StagingConfig(Config):
    """StagingConfig."""

    DEBUG = True


class ProductionConfig(Config):
    """ProductionConfig."""

    DEBUG = False
    TESTING = False
    DATABASE_URL = "host='localhost' port='5432' dbname='data' user='brian'"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "production": ProductionConfig
}
