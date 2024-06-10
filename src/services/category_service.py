from models.category import Category

from services.upload_service import UploadService
from utils.category_utils import CategoryUtils
from utils.camel_case_utils import CamelCaseUtils

upload_service = UploadService()

class CategoryService:
  file_key = 'datasets/categories.csv'

  def add_category(self, category) -> Category:
    categories_file_exists = upload_service.file_exists(CategoryService.file_key)

    category_csv = CategoryUtils.to_csv(category)

    if categories_file_exists:
      categories_csv = upload_service.read_text_file(CategoryService.file_key)
      csv = f'{categories_csv}\n{category_csv}'

      upload_service.write_text_to_file(csv, CategoryService.file_key)

    else:
      category_header_csv = ','.join(map(lambda attribute: f'"{CamelCaseUtils.to_camel_case(attribute)}"', Category.attributes))
      csv = f'{category_header_csv}\n{category_csv}'

      upload_service.write_text_to_file(csv, CategoryService.file_key)

    return category
