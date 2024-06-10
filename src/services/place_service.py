from enums.dataset_file_key_enum import DatasetFileKeyEnum
from utils.place_utils import PlaceUtils
from utils.camel_case_utils import CamelCaseUtils
from models.place import Place

from services.upload_service import UploadService

upload_service = UploadService()

class PlaceService:
  def add_place(self, place: Place) -> Place:
    places_file_exists = upload_service.file_exists(DatasetFileKeyEnum.PLACES.value)

    place_csv = PlaceUtils.to_csv(place)

    if places_file_exists:
      places_csv = upload_service.read_text_file(DatasetFileKeyEnum.PLACES.value)
      csv = f'{places_csv}\n{place_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.PLACES.value)

    else:
      place_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', Place.attributes))
      csv = f'{place_header_csv}\n{place_csv}'

      upload_service.write_text_to_file(csv, DatasetFileKeyEnum.PLACES.value)

    return place
