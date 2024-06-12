import json
from typing import Dict
from io import StringIO
import pandas as pd

from models.event import Event
from utils.csv_utils import CsvUtils

class EventUtils:
  @staticmethod
  def from_dict(dict: Dict) -> Event:
    return Event(
      id = dict['id'],
      start_date = dict['startDate'],
      end_date = dict['endDate'],
      categories = dict['categories'],
      total_tickets_count = dict['totalTicketsCount'],
      sold_tickets_count = dict['soldTicketsCount'],
      place_id = dict['placeId'],
      created_at = dict['createdAt'],
      updated_at = dict['updatedAt'],
    )

  @staticmethod
  def from_csv_to_data_frame(events_csv: str):
    csv_file = StringIO(events_csv)
    data_frame = pd.read_csv(csv_file)

    return data_frame

  @staticmethod
  def to_csv(event):
    attributes = filter(lambda attribute: attribute != 'categories', Event.attributes)

    return CsvUtils.to_csv(event, attributes)
