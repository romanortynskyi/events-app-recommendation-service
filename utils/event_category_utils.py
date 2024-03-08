from typing import Dict

from models.event_category import EventCategory
from utils.csv_utils import CsvUtils

class EventCategoryUtils:
  @staticmethod
  def from_dict(dict: Dict) -> EventCategory:
    return EventCategory(
      event_id = dict['eventId'],
      category_id = dict['categoryId'],
    )

  @staticmethod
  def to_csv(event_category):
    return CsvUtils.to_csv(event_category, EventCategory.attributes)
