from flanker.addresslib import address # https://github.com/mailgun/flanker
from typing import Tuple, List

from bkks_volte_notification_sender.notification_details import (
    Attachment,
    NotificationDetails,
    NotificationType,
)
import re


class MessageValidator:
    def __init__(self):
        self.is_valid = True
        self.message = "OK"

    def email_validator(self, to_email_addresses: List[str]) -> Tuple[bool, str]:
        self.__init__()
        for to_email_address in to_email_addresses:
            valid_email_address=address.parse(to_email_address)
            if not valid_email_address:
                self.is_valid = False
                self.message = f"{to_email_address} is not a valid email address"
                break
        return self.is_valid, self.message
    
    def contact_no_validator(self, contact_numbers: List[str]) -> Tuple[bool, str]:
        self.__init__()
  
        for contact_number in contact_numbers:
            if not bool(re.match(r'^\+\d{8,20}$', contact_number)):
               self.is_valid = False
               self.message= f"{contact_number} is an invalid contact number, valid contact number should have a country code and only digits(8-20 digits), example +4743644444"
               break
        return self.is_valid, self.message

    def attachment_validator(self, attachments: List[Attachment]):
        self.__init__()

        for attachment in attachments:
            if not bool(re.match(r'^[\w,-]+\.\w+$', attachment.file_name)):
                self.is_valid = False
                self.message = f"{attachment.file_name} is an invalid attachment file name, valid file name must contain a file extension and can contain only alphanumeric characters, hyphen or underscore"
            if not bool(re.match(r'^(https?:\/\/)?([\w\.-]+\.[a-z\.]{2,6}|[\d\.]+)([\/:?=&#]{1}[\w\.-]+)*[\/\?]?$', attachment.url)):
                self.is_valid = False
                self.message = f"{attachment.url} is an invalid url"
        return self.is_valid, self.message

    def notification_type_enum_validator(
        self, notification_type: str
    ) -> Tuple[bool, str]:
        self.__init__()
        if not notification_type in NotificationType.__members__:
            self.is_valid = False
            self.message = f"Enum values should be one of values from {NotificationType._member_names_}"
        return self.is_valid, self.message

    def email_and_contact_no_null_validator(self, to_email_address, contact_no):
        self.__init__()
        if not (to_email_address or contact_no):
            self.message = "Please provide either email or contact_no"
            self.is_valid = False
        return self.is_valid, self.message

    def notification_type_contact_details_check(
        self,
        notification_type,
        to_email_address,
        contact_no,
        from_email_address,
        contact_source,
    ):
        self.__init__()
        if notification_type == NotificationType.SMS.name:
            if contact_no is None or contact_source is None:
                self.message = (
                    "contact_no" if not contact_no else "contact_source"
                ) + " can not be null"
                self.is_valid = False
        elif notification_type == NotificationType.EMAIL.name:
            if to_email_address is None or from_email_address is None:
                self.message = (
                    "to_email_address "
                    if not to_email_address
                    else "from_email_address"
                ) + " can not be null"
                self.is_valid = False
        return self.is_valid, self.message

    def validate(self, request: NotificationDetails) -> Tuple[bool, str]:

        # Validate if both to_email_address and contact_no are not null
        is_valid, message = self.email_and_contact_no_null_validator(
            request.to_email_addresses, request.contact_numbers
        )
        if not is_valid:
            return is_valid, message

        # Validate notification type belongs to enum values
        is_valid, message = self.notification_type_enum_validator(
            request.notification_type
        )
        if not is_valid:
            return is_valid, message

        # Validate if to_email is valid if sent by user
        if request.to_email_addresses is not None:
            is_valid, message = self.email_validator(request.to_email_addresses)
            if not is_valid:
                return is_valid, message

        # Validate if from_email is valid if sent by user
        if request.from_email_address is not None:
            is_valid, message = self.email_validator([request.from_email_address])
            if not is_valid:
                return is_valid, message
        
        # Validate if bcc_email is valid if sent by user
        if request.bcc_email_addresses is not None:
            is_valid, message = self.email_validator(request.bcc_email_addresses)
            if not is_valid:
                return is_valid, message
        
        # Validate if phone_no is valid if sent by user
        if request.contact_numbers is not None:
            is_valid, message = self.contact_no_validator(request.contact_numbers)
            if not is_valid:
                return is_valid, message

        if request.attachments:
            is_valid, message = self.attachment_validator(request.attachments)
            if not is_valid:
                return is_valid, message

        # Validate contact information null check for notification type
        is_valid, message = self.notification_type_contact_details_check(
            request.notification_type,
            request.to_email_addresses,
            request.contact_numbers,
            request.from_email_address,
            request.contact_source,
        )
        if not is_valid:
            return is_valid, message

        return is_valid, message
