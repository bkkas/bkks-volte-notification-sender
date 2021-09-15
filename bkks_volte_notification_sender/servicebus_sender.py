from bkks_volte_notification_sender.notification_details import (
    NotificationDetails,
    NotificationType,
)
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from email_validator import validate_email, EmailNotValidError


class ServiceBusMessageSender:
    def __init__(self, connection_string: str, queue_name: str):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=self.connection_string, logging_enable=True
        )

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
                        queue_name=self.queue_name
                    )
                    with sender:
                        message = ServiceBusMessage(request.to_json(request))
                        # send the message to the queue
                        sender.send_messages(message)
                        return "OK"
            except Exception as ex:
                return ex
        else:
            return message

    def __validate(self, request: NotificationDetails) -> tuple[bool, str]:
        is_valid = True
        message = ""
        if not request.email_address and not request.phone_no:
            message = "Please pass either email or mobile_no"
            is_valid = False
        elif not request.notification_type in NotificationType.__members__:
            is_valid = False
            message = f"Enum values should be one of values from {NotificationType._member_names_}"
        else:
            try:
                validate_email(request.email_address)
            except EmailNotValidError as e:
                # email is not valid, exception message is human-readable
                message = str(e)
                is_valid = False
        return is_valid, message
