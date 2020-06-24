import os

# Consider switching this to using dotenv

_DB_HOST = os.environ.get("DB_HOST", "users-db")
_DB_MODE = os.environ.get("DB_MODE", "postgresql")
_DB_NAME = os.environ.get("DB_NAME", "users_dev")
_DB_PASS = os.environ.get("POSTGRES_PASSWORD", "FLASK_PASS")
_DB_PORT = os.environ.get("DB_PORT", "users-db")
_DB_USER = os.environ.get("POSTGRES_USER", "FLASK_USER")
SSL_MODE = os.environ.get("SSL_MODE", False)


class BaseConfig:
    """Fallback default configuration"""

    DEBUG = False
    EXPLAIN_TEMPLATE_LOADING = False
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    # PREFERRED_URL_SCHEME = "https"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PROPAGATE_EXCEPTIONS = False
    RESTX_MASK_SWAGGER = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "Super Cat Spy Key")
    # E.g. postgresql://{DB_USER}:{DB_PASS}@users-db:5432/users_dev
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "{MODE}://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}{OPTIONS}".format(
            DBNAME=_DB_NAME,
            HOST=_DB_HOST,
            MODE=_DB_MODE,
            PASS=_DB_PASS,
            PORT=_DB_PORT,
            USER=_DB_USER,
            OPTIONS="?sslmode=require" if SSL_MODE else "",
        ),
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
