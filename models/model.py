from dataclasses import dataclass
from datetime import datetime

@dataclass
class Model:
  id: int
  created_at: datetime
  updated_at: datetime