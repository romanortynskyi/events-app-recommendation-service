from dataclasses import dataclass
from datetime import datetime
from typing import List

from models.model import Model
from models.user import User

@dataclass
class Event(Model):
  attributes = ['id', 'title', 'description', 'start_date', 'end_date', 'ticket_price', 'author_id', 'image_id', 'place_id', 'created_at', 'updated_at']
  title: str
  description: str
  start_date: datetime
  end_date: datetime
  ticket_price: float
  author_id: int
  image_id: int
  place_id: int
  categories: List[int]
