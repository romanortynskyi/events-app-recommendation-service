import json
from typing import Dict, List
import csv
import io

import pandas as pd

from models.event import Event
from models.user import User

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
  def read_csv(events_csv: str):
    csv_file = io.StringIO(events_csv)
    data = pd.read_csv(csv_file)

    data['categories'] = data['categories'].apply(lambda categoriesJSON: json.loads(categoriesJSON))

    return data
