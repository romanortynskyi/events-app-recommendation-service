from dataclasses import dataclass
from datetime import datetime
from typing import List

from models.model import Model
from models.user import User

@dataclass
class Event(Model):
  title: str
  description: str
  start_date: datetime
  end_date: datetime
  ticket_price: float
  author_id: int
  categories: List[int]