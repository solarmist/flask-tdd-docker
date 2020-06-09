# https://flask.palletsprojects.com/en/1.1.x/tutorial/install/
from setuptools import find_packages, setup

setup(
    name="Your Application",
    author="Joshua Olson",
    version="1.0",
    long_description=__doc__,
    license=open("LICENSE").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask",
        "Flask-RESTX",
        "werkzeug",
        "Flask-SQLAlchemy",
        "psycopg2-binary",
        "pytest",
    ],
)
