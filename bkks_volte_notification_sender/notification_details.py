from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class NotificationDetails:
    notification_type: str
    subject: str
    message: str
    email_address: str = None
    phone_no: str = None
    is_delivered: bool = False
    has_attachment: bool = False
    retry_count: int = 0
    created: datetime = datetime.utcnow().isoformat()
    last_modified: datetime = datetime.utcnow().isoformat()

    def __defaultconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def to_json(self, request) -> str:
        json.dumps(request.__dict__, default=self.__defaultconverter)
