from setuptools import setup

setup(
    name='bkks-volte-notification-sender',
    version='0.1',
    description='My private package from private github repo',
    url='git@github.com:bkkas/bkks-volte-notification-sender.git',
    author='Rashmi Kumari,Jesus Gazol',
    author_email='rashmi.kumari@bkk.no',
    license='Volte',
    packages=['bkks-volte-notification-sender'],
    install_requires=[
          'azure-servicebus',
    ],
    zip_safe=False
)