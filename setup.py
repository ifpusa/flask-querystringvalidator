import io
import re

from setuptools import setup

setup(
    name="Flask-QueryStringValidator",
    version=0.2,
    url="https://github.com/ifpusa/flask-querystringvalidator",
    project_urls={
        "Documentation": "https://github.com/ifpusa/flask-querystringvalidator",
        "Code": "https://github.com/ifpusa/flask-querystringvalidator",
        "Issue tracker": "https://github.com/ifpusa/flask-querystringvalidator/issues",
    },
    license="BSD-3-Clause",
    author="Jesse Whitehouse",
    author_email="jesse@whitehouse.dev",
    maintainer="IFPUSA",
    maintainer_email="jwhitehouse@ifpusa.com",
    description="Adds query string validation to your Flask application.",
    long_description='',
    packages=["flask_querystring"],
    include_package_data=True,
    python_requires=">= 3.6",
    install_requires=["Flask>=1.0.4"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
