from modules.ya_disk_upload.ya_disk_uploader import YaDiskUploader
from modules.vk_modules.vk_api import VkProfilePhotosRetriever
from modules.create_json.create_json import create_json_file


class Backup:
	def __init__(self, user_id: int, album_id: str = 'profile', count: int = 5) -> None:
		data = VkProfilePhotosRetriever('photos.get', user_id, album_id, count)
		self.full_info = data.get_photos_info()['full_info']
		self.json = data.get_photos_info()['json']

	def upload(self, album_id: str = 'profile') -> None:
		ya_disk_uploader = YaDiskUploader(self.full_info)
		ya_disk_uploader.create_folder_process(album_id)

	def create_json(self) -> None:
		create_json_file(self.json)


backup_photos_from_vk = Backup(133468233, 'profile', 12)
backup_photos_from_vk.upload()
# backup_photos_from_vk.create_json()
