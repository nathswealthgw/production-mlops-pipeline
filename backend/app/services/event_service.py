import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class EventService:
    def publish_prediction_event(self, request: dict, response: dict) -> None:
        message = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "request": request,
            "response": response,
        }
        logger.info("prediction_event=%s", json.dumps(message))


event_service = EventService()
