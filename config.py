"""Docsstring for config.py."""
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
    DATABASE_URL = os.getenv('DATABASE_DEVELOP')


class TestingConfig(Config):
    """TestingConfig."""

    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_TEST')


class StagingConfig(Config):
    """StagingConfig."""

    DEBUG = True


class ProductionConfig(Config):
    """ProductionConfig."""

    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_PRODUCTION')


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "production": ProductionConfig
}
