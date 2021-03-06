# https://flask.palletsprojects.com/en/1.1.x/tutorial/install/
from setuptools import find_namespace_packages, setup

setup(
    name="flask_tdd_docker",
    author="Joshua Olson",
    version="1.0",
    long_description=__doc__,
    license=open("LICENSE").read(),
    packages=find_namespace_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask-Admin",
        "Flask-RESTX",
        "Flask-SQLAlchemy",
        "Flask-Cors",
        "Flask",
        "gunicorn",
        "psycopg2-binary",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "werkzeug",
    ],
)
