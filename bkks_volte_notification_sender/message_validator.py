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
            self.message = "Please provide either email or contact_no"
            self.is_valid = False
        return self.is_valid, self.message

    def notification_type_contact_details_check(
        self, notification_type, email_address, contact_no
    ):
        self.__init__()
        if notification_type == NotificationType.sms.name and contact_no is None:
            self.message = "Contact_no cannot be null for sms notification_type"
            self.is_valid = False
        elif notification_type == NotificationType.email.name and email_address is None:
            self.message = "Email_address cannot be null for email notification_type"
            self.is_valid = False
        return self.is_valid, self.message

    def validate(self, request: NotificationDetails) -> tuple[bool, str]:

        # Validate if both email_address and contact_no are not null
        is_valid, message = self.email_and_contact_no_null_validator(
            request.email_address, request.contact_no
        )
        if not is_valid:
            return is_valid, message

        # Validate notification type belongs to enum values
        is_valid, message = self.notification_type_enum_validator(
            request.notification_type
        )
        if not is_valid:
            return is_valid, message

        # Validate if email is valid if sent by user
        if request.email_address is not None:
            is_valid, message = self.email_validator(request.email_address)
            if not is_valid:
                return is_valid, message

        # Validate contact information null check for notification type
        is_valid, message = self.notification_type_contact_details_check(
            request.notification_type, request.email_address, request.contact_no
        )
        if not is_valid:
            return is_valid, message

        return is_valid, message
