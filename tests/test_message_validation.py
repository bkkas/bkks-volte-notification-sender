import unittest

from bkks_volte_notification_sender.message_validator import MessageValidator
from bkks_volte_notification_sender.notification_details import Attachment


class TestMessageValidation(unittest.TestCase):

    message_validator = MessageValidator()

    def test_invalid_email_validation(self):
        email_addresses = ["test1@", "test2"]
        self.assertFalse(self.message_validator.email_validator(email_addresses)[0])

    def test_valid_email_validation(self):
        email_addresses = ["test1@bkk.no", "test2@bkk.no"]
        self.assertTrue(self.message_validator.email_validator(email_addresses)[0])

    def test_invalid_enum_value_for_notification_type(self):
        notification_type = "invalid"
        self.assertFalse(
            self.message_validator.notification_type_enum_validator(notification_type)[0],
        )

    def test_valid_enum_value_for_notification_type(self):
        notification_type = "SMS"
        self.assertTrue(
            self.message_validator.notification_type_enum_validator(notification_type)[0],
        )

    def test_invalid_attachments(self):
        attachments = [
            Attachment(file_name="filename with-space.ext", url="https://bla.no"),
            Attachment(file_name="filename-without-extension", url="https://bla.no"),
            Attachment(file_name="filename.txt", url="htt://bla.no"),
            Attachment(file_name="filename.txt", url="https:/bla.no"),
            Attachment(file_name="filename.txt", url="https://bla"),
        ]
        for attachment in attachments:
            self.assertFalse(
                self.message_validator.attachment_validator([attachment])[0],
                msg=f"Attachment not invalid: {attachment}"
            )

    def test_valid_attachments(self):
        attachments = [
            Attachment(file_name="filename.ext", url="http://bla.no"),
            Attachment(file_name="filename.ext", url="https://bla.no"),
            Attachment(file_name="filename.ext", url="bla.no"),
            Attachment(file_name="filename-09_abcd.ext", url="https://www.bla.no/path/05?id=123"),
        ]
        self.assertTrue(self.message_validator.attachment_validator(attachments)[0])


if __name__ == "__main__":
    unittest.main()
