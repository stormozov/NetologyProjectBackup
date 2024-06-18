import configparser
import requests
from modules.vk_modules.vk_photo_processor import VKPhotoProcessor


class VkProfilePhotosRetriever(VKPhotoProcessor):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    vk_api = config['VK_API']
    API_VERSION: int = vk_api['Api_version']
    URL: str = vk_api['Url']
    TOKEN: str = vk_api['Token']
    DATE_FORMAT: str = '%Y-%m-%d'
    PREFERRED_SIZES = ['w', 'z']

    def __init__(self, method: str, user_id: int, album_id: str = 'wall', count: int = 5) -> None:
        self.method = method
        self.params = {
            'access_token': self.TOKEN,
            'owner_id': user_id,
            'album_id': album_id,
            'count': count,
            'extended': 1,
            'photo_sizes': 1,
            'v': self.API_VERSION,
        }

    def retrieve_photo_data(self):
        try:
            response = requests.get(self.URL + self.method, params=self.params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during HTTP request: {e}")
            return None

    def get_photos(self):
        response = self.retrieve_photo_data()
        if 'response' in response and 'items' in response['response']:
            photos = response['response']['items']
            photo_list = self._extract_photo_info(photos, self.DATE_FORMAT, self.PREFERRED_SIZES)
            return photo_list
        else:
            return []


test = VkProfilePhotosRetriever('photos.get', 133468233, 'profile', 2).get_photos()
