from email_validator import EmailNotValidError, validate_email

from bkks_volte_notification_sender.notification_details import NotificationDetails, NotificationType


class MessageValidator:
    def __init__(self):
        self.is_valid = True
        self.message = "OK"

    def email_validator(self, to_email_addresses) -> tuple[bool, str]:
        self.__init__()
        for to_email_address in to_email_addresses:
            try:
                validate_email(to_email_address)
            except EmailNotValidError as e:
                # email is not valid, exception message is human-readable
                self.is_valid = False
                self.message = str(e)
                break
        return self.is_valid, self.message

    def notification_type_enum_validator(self, notification_type: str) -> tuple[bool, str]:
        self.__init__()
        if not notification_type in NotificationType.__members__:
            self.is_valid = False
            self.message = f"Enum values should be one of values from {NotificationType._member_names_}"
        return self.is_valid, self.message

    def email_and_contact_no_null_validator(self, to_email_address, contact_no):
        self.__init__()
        if not to_email_address and contact_no:
            self.message = "Please provide either email or contact_no"
            self.is_valid = False
        return self.is_valid, self.message

    def notification_type_contact_details_check(self, notification_type, to_email_address, contact_no):
        self.__init__()
        if notification_type == NotificationType.sms.name and contact_no is None:
            self.message = "Contact_no cannot be null for sms notification_type"
            self.is_valid = False
        elif notification_type == NotificationType.email.name and to_email_address is None:
            self.message = "to_email_address cannot be null for email notification_type"
            self.is_valid = False
        return self.is_valid, self.message

    def validate(self, request: NotificationDetails) -> tuple[bool, str]:

        # Validate if both to_email_address and contact_no are not null
        is_valid, message = self.email_and_contact_no_null_validator(
            request.to_email_addresses, request.contact_numbers
        )
        if not is_valid:
            return is_valid, message

        # Validate notification type belongs to enum values
        is_valid, message = self.notification_type_enum_validator(request.notification_type)
        if not is_valid:
            return is_valid, message

        # Validate if email is valid if sent by user
        if request.to_email_addresses is not None:
            is_valid, message = self.email_validator(request.to_email_addresses)
            if not is_valid:
                return is_valid, message

        # Validate contact information null check for notification type
        is_valid, message = self.notification_type_contact_details_check(
            request.notification_type, request.to_email_addresses, request.contact_numbers
        )
        if not is_valid:
            return is_valid, message

        return is_valid, message
