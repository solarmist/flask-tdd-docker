import os

# Consider switching this to using dotenv

_DB_USER = os.environ.get("POSTGRES_USER", "FLASK_USER")
_DB_PASS = os.environ.get("POSTGRES_PASSWORD", "FLASK_PASS")


class BaseConfig:
    """Fallback default configuration"""

    DEBUG = False
    EXPLAIN_TEMPLATE_LOADING = False
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    PREFERRED_URL_SCHEME = "https"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PROPAGATE_EXCEPTIONS = False
    RESTX_MASK_SWAGGER = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "Super Cat Spy Key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").format(
        DB_USER=_DB_USER, DB_PASS=_DB_PASS
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True


class TestingConfig(BaseConfig):
    """Configuration for running tests"""

    JSONIFY_PRETTYPRINT_REGULAR = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    TESTING = False
