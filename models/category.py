from dataclasses import dataclass

from models.model import Model

@dataclass
class Category(Model):
  attributes = ['id', 'events_count', 'created_at', 'updated_at']
  events_count: int
