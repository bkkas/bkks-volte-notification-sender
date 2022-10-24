import dataclasses
import enum
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class NotificationType(enum.Enum):
    EMAIL = 1
    SMS = 2


@dataclass
class Attachment:
    file_name: str
    url: str

@dataclass
class NotificationDetails:
    notification_type: NotificationType
    subject: str
    message: str
    from_email_address: str = None
    to_email_addresses: Optional[List[str]] = None
    bcc_email_addresses: Optional[List[str]] = None
    contact_numbers: Optional[List[str]] = None
    contact_source: str = None
    is_delivered: bool = False
    has_attachment: bool = False
    attachments: Optional[List[Attachment]] = None
    retry_count: int = 0
    event_timestamp: str =None
    def __defaultconverter(self, o):
        
        if isinstance(o, datetime):
            return o.__str__()

    def to_json(self, request) -> str:
        return json.dumps(request.__dict__, default=self.__defaultconverter)
    


class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            if isinstance(o, datetime):
                return o.__str__()
            return super().default(o)