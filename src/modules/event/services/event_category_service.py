from enums.dataset_file_key_enum import DatasetFileKeyEnum
from models.event_category import EventCategory
from services.upload_service import UploadService
from utils.camel_case_utils import CamelCaseUtils
from utils.event_category_utils import EventCategoryUtils

upload_service = UploadService()

class EventCategoryService:
  def add_event_category(self, event_category: EventCategory) -> EventCategory:
    event_categories_file_exists = upload_service.file_exists(DatasetFileKeyEnum.EVENT_CATEGORIES.value)

    event_category_csv = EventCategoryUtils.to_csv(event_category)

    if event_categories_file_exists:
      event_categories_csv = upload_service.read_text_file(DatasetFileKeyEnum.EVENT_CATEGORIES.value)
      csv = f'{event_categories_csv}\n{event_category_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.EVENT_CATEGORIES.value)

    else:
      event_category_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', EventCategory.attributes))
      csv = f'{event_category_header_csv}\n{event_category_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.EVENT_CATEGORIES.value)

    return event_category
