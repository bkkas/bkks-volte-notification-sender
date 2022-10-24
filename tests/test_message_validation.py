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

    def test_attachments(self):
        attachments = [
            (Attachment(file_name="filename with-space.ext", url="https://bla.no"), False),
            (Attachment(file_name="filename-without-extension", url="https://bla.no"), False),
            (Attachment(file_name="filename.txt", url="htt://bla.no"), False),
            (Attachment(file_name="filename.txt", url="https:/bla.no"), False),
            (Attachment(file_name="filename.txt", url="https://bla"), False),
            (Attachment(file_name="filename.ext", url="bla.no"), False),
            (Attachment(file_name="filename.ext", url="http://bla.no"), True),
            (Attachment(file_name="filename.ext", url="https://bla.no"), True),
            (Attachment(file_name="filename-09_abcd.ext", url="https://www.bla.no/path/05?id=123"), True),
            (Attachment(file_name="filename-09_abcd.ext", url="https://www.bla.no/path_to_file/05/file_name.pdf"), True),
        ]

        for (attachment, expected_result) in attachments:
            is_valid, msg = self.message_validator.attachment_validator([attachment])
            self.assertEqual(
                is_valid,
                expected_result,
                msg=msg
            )

if __name__ == "__main__":
    unittest.main()
