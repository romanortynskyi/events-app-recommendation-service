from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar('T')

@dataclass
class Paginated(Generic[T]):
  items: List[T]
  total_pages_count: int
  total_items_count: int
