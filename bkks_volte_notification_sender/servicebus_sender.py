from bkks_volte_notification_sender.message_validator import MessageValidator
from bkks_volte_notification_sender.notification_details import (
    NotificationDetails,
)
from azure.servicebus import ServiceBusClient, ServiceBusMessage


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
            email_address: str: recipient email adress
            phone_no: str: recipient phone number
        notification_type, subject, message and (email_address or phone_no) are mandatory parameters
        """
        is_valid, message = self.__validate(request)
        if is_valid:
            try:
                with self.servicebus_client:
                    sender = self.servicebus_client.get_queue_sender(
                        queue_name=self.servicebus_client._entity_name
                    )
                    with sender:
                        json_message=request.to_json(request)
                        message = ServiceBusMessage("Hello")
                        # send the message to the queue
                        sender.send_messages(message)
                        return "OK"
            except Exception as ex:
                return ex
        else:
            return message

    def __validate(self, request: NotificationDetails) -> tuple[bool, str]:
        return self.message_validator.validate(request)
