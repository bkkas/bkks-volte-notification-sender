from setuptools import setup

setup(
    name="bkks_volte_notification_sender",
    version="0.8.4",
    description="A simple package to send messages to a queue azure service bus",
    license="LGPL3",
    url="git@github.com:bkkas/bkks-volte-notification-sender.git",
    author="bkks-volte",
    author_email="rashmi.kumari@bkk.no,",
    packages=["bkks_volte_notification_sender"],
    install_requires=[
        "azure-servicebus",
        "email-validator",
    ],
    zip_safe=False,
)
