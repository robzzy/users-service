#!/usr/bin/env python3
from setuptools import find_packages, setup


setup(
    name="users",
    version="0.0.1",
    description="Manage users",
    packages=find_packages("src", exclude=["test", "test.*", "db"]),
    package_dir={"": "src"},
    install_requires=[
        "alembic==1.0.10",
        "nameko==3.0.0-rc8",
        "nameko-sqlalchemy==1.5.0",
        "nameko-tracer==1.2.0",
        "nameko-autocrud==0.2.0",
        "mysql-connector-python==8.0.16",
        "pyjwt==2.4.0",
        "marshmallow==2.19.5",
    ],
    extras_require={
        "dev": [
            "coverage==4.5.3",
            "flake8>=3.7.7",
            "pytest==4.5.0",
            "behave==1.2.5",
            "black==19.10b0",
        ],
    },
    zip_safe=True
)
