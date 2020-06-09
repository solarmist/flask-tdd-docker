import os

# Consider switching this to using dotenv

DB_USER = os.environ.get("POSTGRESQL_USER")
DB_PASS = os.environ.get("POSTGRESQL_PASSWORD")


class BaseConfig:
    """Fallback default configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").format(
        DB_USER=DB_USER, DB_PASS=DB_PASS
    )


class TestingConfig(BaseConfig):
    """Configuration for running tests"""

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL").format(
        DB_USER=DB_USER, DB_PASS=DB_PASS
    )


class ProductionConfig(BaseConfig):
    """Production configuration"""

    TESTING = False
    POSTGRESQL_USER = os.environ.get("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").format(
        DB_USER=DB_USER, DB_PASS=DB_PASS
    )
