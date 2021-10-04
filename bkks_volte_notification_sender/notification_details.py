import enum
import json
from dataclasses import dataclass
from datetime import datetime


class NotificationType(enum.Enum):
    email = 1
    sms = 2


@dataclass
class NotificationDetails:
    notification_type: NotificationType
    subject: str
    message: str
    from_email_address: str = "noreply@volte.no"
    to_email_addresses: list = None
    contact_numbers: list = None
    is_delivered: bool = False
    has_attachment: bool = False
    retry_count: int = 0
    event_timestamp: datetime = datetime.utcnow().isoformat()

    def __defaultconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def to_json(self, request) -> str:
        json.dumps(request.__dict__, default=self.__defaultconverter)
