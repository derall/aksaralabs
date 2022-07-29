from setuptools import setup,find_packages

setup(
    name='aksaralabs',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    scripts=['aksaralabs/bin/aksaralabs'],
    version='0.1.0',
    author='aksaralabs studio',
    author_email='derall.santo@gmail.com',
    install_requires=[
        'colorama==0.3.9',
        'flask==0.12.2',
        'flask-appbuilder==4.1.3',
        'flask-cache==0.13.1',
        'flask-migrate==2.1.1',
        'flask-script==2.0.6',
        'flask-sqlalchemy==2.1',
    ],
)