from dataclasses import dataclass
import json
from typing import List

from models.model import Model

@dataclass
class User(Model):
  first_name: str
  last_name: str
  categories: List[int]

  @staticmethod
  def from_csv(line):
    categories = json.loads(line['categories'])
    
    return User(
      id = int(line['id']),
      first_name = line['firstName'],
      last_name = line['lastName'],
      created_at = line['createdAt'],
      updated_at = line['updatedAt'],
      categories = categories,
    )