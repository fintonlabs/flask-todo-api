from setuptools import setup, find_packages

setup(
    name='flask-todo-api',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlite3'
    ],
    entry_points={
        'console_scripts': [
            'flask-todo-api=main:main',
        ],
    },
)