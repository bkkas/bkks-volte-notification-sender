from bkks_volte_notification_sender.notification_details import NotificationDetails
from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBusMessageSender:
    def __init__(self, connection_string: str, queue_name: str):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=self.connection_string, logging_enable=True
        )

    def send_single_message(self, request:NotificationDetails) -> str:
        # create a Service Bus message
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
