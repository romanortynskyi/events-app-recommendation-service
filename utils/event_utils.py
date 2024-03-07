import json
from typing import Dict
import io
import pandas as pd

from models.event import Event

class EventUtils:
  @staticmethod
  def from_dict(dict: Dict) -> Event:
    return Event(
      id = dict['id'],
      title = dict['title'],
      description = dict['description'],
      ticket_price = dict['ticketPrice'],
      start_date = dict['startDate'],
      end_date = dict['endDate'],
      categories = dict['categories'],
      author_id = dict['authorId'],
      created_at = dict['createdAt'],
      updated_at = dict['updatedAt'],
    )

  @staticmethod
  def from_csv_to_data_frame(events_csv: str):
    csv_file = io.StringIO(events_csv)
    data_frame = pd.read_csv(csv_file)

    data_frame['categories'] = data_frame['categories'].apply(lambda categoriesJSON: json.loads(categoriesJSON))

    return data_frame
