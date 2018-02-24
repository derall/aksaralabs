from setuptools import setup,find_packages

setup(
    name='aksaralabs',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    scripts=['aksaralabs/bin/aksaralabs'],
    version="0.1.0",
    author="aksaralabs studio",
    author_email="derall.santo@gmail.com",
    install_requires=[
        'flask',
    ],
)