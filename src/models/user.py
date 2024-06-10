from dataclasses import dataclass
from typing import List

from models.model import Model

@dataclass
class User(Model):
  first_name: str
  last_name: str
  categories: List[int]
