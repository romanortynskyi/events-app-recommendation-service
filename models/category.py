from dataclasses import dataclass

from models.model import Model

@dataclass
class Category(Model):
  attributes = ['id', 'name', 'events_count', 'created_at', 'updated_at']
  name: str
  events_count: int