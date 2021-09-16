from email_validator import validate_email, EmailNotValidError
from bkks_volte_notification_sender.notification_details import (
    NotificationType,
    NotificationDetails,
)


class MessageValidator:
    def __init__(self):
        self.is_valid = True
        self.message = "OK"

    def email_validator(self, email_address: str) -> tuple[bool, str]:
        self.__init__()
        try:
            validate_email(email_address)
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            self.is_valid = False
            self.message = str(e)
        return self.is_valid, self.message

    def notification_type_enum_validator(
        self, notification_type: str
    ) -> tuple[bool, str]:
        self.__init__()
        if not notification_type in NotificationType.__members__:
            self.is_valid = False
            self.message = f"Enum values should be one of values from {NotificationType._member_names_}"
        return self.is_valid, self.message

    def email_and_contact_no_null_validator(self, email_address, contact_no):
        self.__init__()
        if not email_address and contact_no:
            self.message = "Please pass either email or contact_no"
            self.is_valid = False
        return self.is_valid, self.message

    def validate(self, request: NotificationDetails) -> tuple[bool, str]:
        is_valid, message = self.email_and_contact_no_null_validator(
            request.email_address, request.contact_no
        )
        if not is_valid:
            return is_valid, message

        is_valid, message = self.email_validator(request.email_address)
        if not is_valid:
            return is_valid, message

        is_valid, message = self.notification_type_enum_validator(
            request.notification_type
        )
        if not is_valid:
            return is_valid, message
        return is_valid, message
