from setuptools import setup, find_packages

setup(
    name='flask-todo-api',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==1.1.2',
        'Flask-SQLAlchemy==2.5.1'
    ]
)