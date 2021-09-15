# bkks-volte-notification-sender

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

This package helps to send data to azure service bus.

## Installing

```
pip install git+https://github.com/bkkas/bkks-volte-notification-sender.git
```

## Use

notification_details=NotificationDetails(
    message="<notification_message>",
    notification_type="<notification_type>",
    subject="<notification_subject>",
    email_address="<email_address>"
)
sender=ServiceBusMessageSender("<connection_strin>","<queue_name>")
message=sender.send_single_message(notification_details)
print(message)