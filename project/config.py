import os

# Consider switching this to using dotenv


class BaseConfig:
    """Fallback default configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Configuration for running tests"""

    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Production configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("DATABASE_URL")
