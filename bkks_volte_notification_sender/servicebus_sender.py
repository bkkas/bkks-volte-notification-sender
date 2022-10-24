from datetime import datetime
import json

from azure.servicebus import ServiceBusClient, ServiceBusMessage

from bkks_volte_notification_sender.message_validator import MessageValidator
from bkks_volte_notification_sender.notification_details import JSONEncoder, NotificationDetails
from typing import Tuple


class ServiceBusMessageSender:
    def __init__(self, servicebus_client: ServiceBusClient):
        self.servicebus_client = servicebus_client
        self.message_validator = MessageValidator()

    def send_single_message(self, request: NotificationDetails) -> str:
        """
        Takes NotificationDetails as an argument.
        Args:
        NotificationDetails:
            notification_type: Enum: NotificationType
            subject: str: message/notification subject
            message: str: message/notification body
            from_email_address: list: list of recipient email addresses
            contact_no: list: list of recipient contact no
        notification_type, subject, message and (from_email_address or contact_no) are mandatory parameters
        """
        is_valid, message = self.__validate(request)
        if is_valid:
            try:
                with self.servicebus_client:
                    sender = self.servicebus_client.get_queue_sender(queue_name=self.servicebus_client._entity_name)
                    request.event_timestamp= datetime.utcnow().isoformat()
                    with sender:
                        jsonStr = json.dumps(request,cls=JSONEncoder)
                        message = ServiceBusMessage(jsonStr)
                        # send the message to the queue
                        sender.send_messages(message)
                        return "OK"
            except Exception as ex:
                return str(ex)
        else:
            return message

    def __validate(self, request: NotificationDetails) -> Tuple[bool, str]:
        return self.message_validator.validate(request)
