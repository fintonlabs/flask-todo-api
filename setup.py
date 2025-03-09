from setuptools import setup, find_packages

setup(
    name='flask-todo-api',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==1.1.2',
        'Flask-SQLAlchemy==2.4.4',
        'Flask-JWT-Extended==3.24.1',
        'Werkzeug==1.0.1'
    ]
)