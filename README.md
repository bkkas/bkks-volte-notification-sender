# bkks-volte-notification-sender

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

This package helps to send data to a queue data on azure service bus.

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

service_bus_client = ServiceBusClient.from_connection_string(
    conn_str=<connection_string>,
    entity_name=<queue_name>,
)
sender=ServiceBusMessageSender(service_bus_client)
respose=sender.send_single_message(notification_details)

The response should be "OK" if the message has been sent to queue else we should get error details.
