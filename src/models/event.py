from dataclasses import dataclass
from datetime import datetime
from typing import List

from models.model import Model
from models.user import User

@dataclass
class Event(Model):
  attributes = [
    'id',
    'start_date',
    'end_date',
    'place_id',
    'categories',
    'total_tickets_count',
    'sold_tickets_count',
  ]

  start_date: datetime
  end_date: datetime
  place_id: int
  categories: List[int]
  total_tickets_count: int
  sold_tickets_count: int
