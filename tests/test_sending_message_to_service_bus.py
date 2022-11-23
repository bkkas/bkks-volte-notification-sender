import unittest

from bkks_volte_notification_sender.notification_details import Attachment,NotificationDetails
from bkks_volte_notification_sender.servicebus_sender import ServiceBusMessageSender


class ServiceBusClientMock:
    def __init__(self):
        self._entity_name = ""

    def get_queue_sender(self, queue_name, **kwargs):
        return ServiceBusSenderMock()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class ServiceBusSenderMock:
    def send_messages(self, *args):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class TestMessageSender(unittest.TestCase):
    def test_sending_invalid_email_message_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_invalid_email_notification_details()
        )
        self.assertNotEqual("OK", message)

    def test_sending_valid_email_message_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_valid_email_notification_details()
        )
        self.assertEqual("OK", message)
    
    def test_sending_invalid_email_message_with_bcc_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_invalid_email_notification_details_with_bcc()
        )
        self.assertNotEqual("OK", message)

    def test_sending_valid_email_message_with_bcc_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_valid_email_notification_details_with_bcc()
        )
        self.assertEqual("OK", message)

    def test_sending_valid_attachment_link_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_valid_attachment_link_notification_details()
        )
        self.assertEqual("OK", message)
    
    def test_sending_invalid_attachment_link_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_invalid_attachment_link_notification_details()
        )
        self.assertNotEqual("OK", message)

    def test_sending_valid_attachment_name_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_valid_attachment_name_notification_details()
        )
        self.assertEqual("OK", message)
    
    def test_sending_invalid_attachment_name_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_invalid_attachment_name_notification_details()
        )
        self.assertNotEqual("OK", message)

    def test_sending_valid_sms_message_to_servicebus(self):
        service_bus_client_mock = ServiceBusClientMock()
        fake_service_bus_message_sender = ServiceBusMessageSender(
            service_bus_client_mock
        )
        message = fake_service_bus_message_sender.send_single_message(
            self.get_valid_sms_notification_details()
        )
        self.assertEqual("OK", message)

    def get_valid_email_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            from_email_address="noreply@volte.no"
        )
    def get_valid_email_notification_details_with_bcc(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            bcc_email_addresses=["test1@bkk.no"],
            from_email_address="Effektvarsling fra Volte hei@volte.no" # We want to add the text with the from email_address
        )

    def get_valid_sms_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="SMS",
            subject="message_test",
            contact_numbers=["+4748631998"],
            contact_source="Volte",
        )

    def get_invalid_email_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@", "test2"],
        )
    def get_invalid_email_notification_details_with_bcc(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@", "test2"],
            bcc_email_addresses=["test1@", "test2"],
        )
    def get_valid_attachment_link_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            from_email_address="noreply@volte.no",
            attachments=[Attachment(file_name="test.pdf",url="https://google.com")]
        )
    def get_invalid_attachment_link_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            from_email_address="noreply@volte.no",
            attachments=[Attachment(file_name="test.pdf",url="http")]
        )
    def get_valid_attachment_name_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            from_email_address="noreply@volte.no",
            attachments=[Attachment(file_name="test.pdf",url="https://google.com")]
        )
    def get_invalid_attachment_name_notification_details(self) -> NotificationDetails:
        return NotificationDetails(
            message="test message",
            notification_type="EMAIL",
            subject="test message",
            to_email_addresses=["test1@bkk.no", "test2@bkk.no"],
            from_email_address="noreply@volte.no",
            attachments=[Attachment(file_name="test",url="https://google.com")]
        )

if __name__ == "__main__":
    unittest.main()
