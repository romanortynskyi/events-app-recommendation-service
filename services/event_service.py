from models.event import Event

from services.upload_service import UploadService

upload_service = UploadService()

class EventService:
  def add_event(self, event) -> Event:
    return event
