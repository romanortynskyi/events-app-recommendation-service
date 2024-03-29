from models.event_category import EventCategory
from services.upload_service import UploadService
from utils.camel_case_utils import CamelCaseUtils
from utils.event_category_utils import EventCategoryUtils

upload_service = UploadService()

class EventCategoryService:
  file_key = 'datasets/event_categories.csv'

  def add_event_category(self, event_category: EventCategory) -> EventCategory:
    event_categories_file_exists = upload_service.file_exists(EventCategoryService.file_key)

    event_category_csv = EventCategoryUtils.to_csv(event_category)

    if event_categories_file_exists:
      event_categories_csv = upload_service.read_text_file(EventCategoryService.file_key)
      csv = f'{event_categories_csv}\n{event_category_csv}'

      upload_service.write_text_to_file(csv, EventCategoryService.file_key)

    else:
      event_category_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', EventCategory.attributes))
      csv = f'{event_category_header_csv}\n{event_category_csv}'

      upload_service.write_text_to_file(csv, EventCategoryService.file_key)

    return event_category
