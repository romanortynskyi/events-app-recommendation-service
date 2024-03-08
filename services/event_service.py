from models.event import Event
from models.event_category import EventCategory

from services.upload_service import UploadService
from services.event_category_service import EventCategoryService
from utils.event_utils import EventUtils
from utils.camel_case_utils import CamelCaseUtils
from utils.event_utils import EventUtils

upload_service = UploadService()
event_category_service = EventCategoryService()

class EventService:
  file_key = 'datasets/events.csv'

  def add_event(self, event: Event) -> Event:
    for category_id in event.categories:
      event_category = EventCategory(
        event_id = event.id,
        category_id = category_id,
      )
      event_category_service.add_event_category(event_category)

    events_file_exists = upload_service.file_exists(EventService.file_key)

    event_csv = EventUtils.to_csv(event)

    if events_file_exists:
      events_csv = upload_service.read_text_file(EventService.file_key)
      csv = f'{events_csv}\n{event_csv}'

      upload_service.write_text_to_file(csv, EventService.file_key)

    else:
      event_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', Event.attributes))
      csv = f'{event_header_csv}\n{event_csv}'

      upload_service.write_text_to_file(csv, EventService.file_key)

    return event
