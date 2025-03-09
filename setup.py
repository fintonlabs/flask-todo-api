from setuptools import setup, find_packages

setup(
    name='todo-flask-api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask==1.1.2',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-JWT-Extended==3.25.1',
        'Werkzeug==1.0.1'
    ],
)