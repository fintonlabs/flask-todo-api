from setuptools import setup

setup(
    name='flask-todo-api',
    version='0.1',
    description='A Flask API for a to-do list application',
    author='Your Name',
    author_email='your.email@example.com',
    packages=['app'],
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'werkzeug',
        'uuid',
        'pyjwt'
    ]
)