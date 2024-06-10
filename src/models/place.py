from dataclasses import dataclass

from models.model import Model

@dataclass
class Place(Model):
  attributes = [
    'id',
    'created_at',
    'updated_at',
  ]
