import requests
import json
from .progress_upload import ProgressUpload

class YandexDiskResources:
    def __init__(self, token: str):
        self._token = token
        self._base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                         'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        """Создание папки"""
        base_url = self._base_url
        headers = self._headers

        response = requests.put(f'{base_url}?path={folder_name}', headers=headers)
        body = json.loads(response.text)

        if response.status_code == 201:
            return True, ''
        elif body['error'] == 'DiskPathPointsToExistentDirectoryError':
            print(f'Folder already created {folder_name}')
            return True, body['message']
        else:
            print(f'Error: {body["error"]}')
            return False, body

    def delete(self, path: str, permanently=True):
        """Удаление папки/файла"""
        base_url = self._base_url
        headers = self._headers

        permanently = 'true' if permanently else 'false'
        response = requests.delete(f'{base_url}?path={path}&force_async=false&permanently={permanently}',
                                   headers=headers)

        if response.status_code == 204:
            return True, ''
        else:
            body = json.loads(response.text)
            print(f'Error: {body["error"]}')
            return False, body

    def get_link_for_download(self, path: str):
        """Получить ссылку для скачивания файла/папки"""
        base_url = self._base_url
        headers = self._headers

        response = requests.get(f'{base_url}/download?path={path}',
                                headers=headers)
        body = json.loads(response.text)

        if response.status_code == 200:
            return True, body['href']
        else:
            print(f'Непредвиденная ошибка: {body["error"]}')
            return False, body

    def upload_file(self, path: str, path_to_file: str, callback):
        """Загрузить файл"""
        link = self._get_upload_link(path)

        if not link[0]:
            return False, link[1]


        response = requests.put(link[1], data=ProgressUpload(callback, path_to_file))

        body = response.json() if len(response.text) != 0 else {}
        body['status_code'] = response.status_code
        return True, body
    def _get_upload_link(self, path):
        """Получить ссылку для загрузки файла"""
        base_url = self._base_url
        headers = self._headers

        response = requests.get(f'{base_url}/upload?path={path}',
                                headers=headers)
        body = response.json()

        if response.status_code == 200:
            return True, body['href']
        else:
            print(f'Непредвиденная ошибка: {body["error"]}')
            return False, body
