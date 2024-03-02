import json
from typing import List
import csv
import io

from models.user import User

class UserUtils:
  @staticmethod
  def _parse_csv_user(line: str) -> User:
    categories = json.loads(line['categories'])
    
    return User(
      id = int(line['id']),
      first_name = line['firstName'],
      last_name = line['lastName'],
      created_at = line['createdAt'],
      updated_at = line['updatedAt'],
      categories = categories,
    )


  @staticmethod
  def parse_csv_users(users_csv: str) -> List[User]:
    users_csv_file = io.StringIO(users_csv)
    csv_reader = csv.DictReader(users_csv_file)

    users = []

    for row in csv_reader:
      user = UserUtils._parse_csv_user(row)
      users.append(user)

    return users