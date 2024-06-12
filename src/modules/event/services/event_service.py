from enums.dataset_file_key_enum import DatasetFileKeyEnum
from models.event import Event
from models.event_category import EventCategory

from services.upload_service import UploadService
from modules.event.services.event_category_service import EventCategoryService
from utils.event_utils import EventUtils
from utils.camel_case_utils import CamelCaseUtils
from utils.event_utils import EventUtils

upload_service = UploadService()
event_category_service = EventCategoryService()

class EventService:
  def add_event(self, event: Event) -> Event:
    for category_id in event.categories:
      event_category = EventCategory(
        event_id = event.id,
        category_id = category_id,
      )
      event_category_service.add_event_category(event_category)

    events_file_exists = upload_service.file_exists(DatasetFileKeyEnum.EVENTS.value)

    event_csv = EventUtils.to_csv(event)

    if events_file_exists:
      events_csv = upload_service.read_text_file(DatasetFileKeyEnum.EVENTS.value)
      csv = f'{events_csv}\n{event_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.EVENTS.value)

    else:
      attributes = filter(lambda attribute: attribute != 'categories', Event.attributes)
      event_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', attributes))
      csv = f'{event_header_csv}\n{event_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.EVENTS.value)

    return event
