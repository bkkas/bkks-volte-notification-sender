from bkks_volte_notification_sender.message_validator import MessageValidator
import unittest


class TestMessageValidation(unittest.TestCase):

    message_validator = MessageValidator()

    def test_invalid_email_validation(self):
        email_address = "test@"
        self.assertFalse(self.message_validator.email_validator(email_address)[0])

    def test_valid_email_validation(self):
        email_address = "test@bkk.no"
        self.assertTrue(self.message_validator.email_validator(email_address)[0])

    def test_invalid_enum_value_for_notification_type(self):
        notification_type = "invalid"
        self.assertFalse(
            self.message_validator.notification_type_enum_validator(notification_type)[
                0
            ],
        )

    def test_valid_enum_value_for_notification_type(self):
        notification_type = "sms"
        self.assertTrue(
            self.message_validator.notification_type_enum_validator(notification_type)[
                0
            ],
        )


if __name__ == "__main__":
    unittest.main()
