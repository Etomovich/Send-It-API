"""Docsstring for config.py."""
import os


class Config(object):
    """docstring for Config."""

    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "brian"


class DevelopmentConfig(Config):
    """docstring for DevelopmentConfig."""

    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_DEVELOP')


class TestingConfig(Config):
    """docstring for TestingConfig."""

    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_TEST')


class StagingConfig(Config):
    """docstring for StagingConfig."""

    DEBUG = True


class ProductionConfig(Config):
    """docstring for ProductionConfig."""

    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_PRODUCTION')


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "production": ProductionConfig
}
