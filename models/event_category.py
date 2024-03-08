from dataclasses import dataclass

@dataclass
class EventCategory:
  attributes = ['event_id', 'category_id']
  event_id: int
  category_id: int
