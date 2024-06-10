from io import StringIO
from typing import Dict
import pandas as pd

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
  
  @staticmethod
  def from_csv_to_data_frame(event_categories_csv: str):
    csv_file = StringIO(event_categories_csv)
    data_frame = pd.read_csv(csv_file)

    return data_frame
