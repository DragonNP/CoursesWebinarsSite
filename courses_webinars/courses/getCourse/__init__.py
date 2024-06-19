import json
from bs4 import BeautifulSoup, NavigableString
import requests


class GetCourse:
    def __init__(self, host):
        self.phpsessid5: str = ''
        self.protocol = 'https://'
        self.host = host
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Host': host,
            'Cache-Control': 'no-cache'
        }

    def login(self, email: str, password: str):
        host = self.host
        protocol = self.protocol
        headers = dict(self.headers)

        request_url = f'{protocol}{host}/cms/system/login'

        response = requests.post(request_url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        body = {
            'action': 'processXdget',
            'xdgetId': soup.find('form').attrs['data-xdget-id'],
            'params[action]': 'login',
            'params[email]': email,
            'params[password]': password
        }

        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Content-Length'] = str(len(body))

        response = requests.post(request_url, data=body, headers=headers)
        try:
            result = json.loads(response.text)
        except json.decoder.JSONDecodeError as e:
            return {'success': False, 'message': 'Данный сайт не поддерживается'}

        if 'errorMessage' in result:
            return {'success': False, 'message': result['errorMessage']}
        self.phpsessid5 = response.cookies['PHPSESSID5']
        self.email = email
        self.password = password

        return {'success': True}

    def get_data_authentications(self) -> dict:
        return {
            'host': self.host,
            'email': self.email,
            'password': self.password
        }

    def get_all_trenings(self):
        phpsessid5 = self.phpsessid5
        protocol = self.protocol
        host = self.host
        headers = self.headers
        if phpsessid5 == '':
            return None

        formatted_data = {}
        response = requests.get(f'{protocol}{host}/cms/system/start?afterLogin=true',
                                cookies={'PHPSESSID5': phpsessid5}, headers=headers)

        for trening in self._get_trenings(response.text):
            if 'lessons' in trening:
                for less in trening['lessons']:
                    formatted_data[less] = trening['lessons'][less]
            elif trening['children']:
                formatted_data[trening['title']] = [self._parse_children(trening['url']), 'module']
            else:
                formatted_data[trening['title']] = [self._parse_lessons(trening['url'], with_data=False), 'module']

        return formatted_data

    def get_info_from_lesson(self, url):
        return self._extract_from_lesson_data(url)

    def _get_trenings(self, html):
        host = self.host
        protocol = self.protocol
        trenings = []

        lessons = self._parse_lessons_from_html(html, with_data=False)
        trenings.append({'lessons': lessons})

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table', class_='stream-table')
        for tr in table.children:
            if type(tr) == NavigableString:
                continue

            class_ = tr.attrs['class'][0]
            if class_ == 'has-children':
                trenings.append({'children': True})
            elif class_ == 'no-children':
                trenings.append({'children': False})
            else:
                print('Произошла ошибка. Объект tr имеет класс:', class_)
                trenings.append({'children': False})

            for td in tr:
                a = td.find('a')
                if type(a) == int:
                    continue
                link = a.attrs['href']
                title = a.select_one('span', class_='stream-title').text

                trenings[-1]['title'] = title
                trenings[-1]['url'] = protocol + host + link
        return trenings

    def _parse_children(self, url):
        phpsessid5 = self.phpsessid5
        headers = self.headers
        formatted_data = {}

        response = requests.get(url, cookies={'PHPSESSID5': phpsessid5}, headers=headers)
        all_trenings = self._get_trenings(response.text)

        for trening in all_trenings:
            if 'lessons' in trening:
                for less in trening['lessons']:
                    formatted_data[less] = trening['lessons'][less]
            elif trening['children']:
                formatted_data[trening['title']] = [self._parse_children(trening['url']), 'module']
            else:
                formatted_data[trening['title']] = [self._parse_lessons(trening['url'], with_data=False), 'module']
        return formatted_data

    def _parse_lessons(self, url, with_data=True):
        phpsessid5 = self.phpsessid5
        headers = self.headers

        response = requests.get(url, cookies={'PHPSESSID5': phpsessid5}, headers=headers)
        html = response.text
        return self._parse_lessons_from_html(html, with_data=with_data)

    def _parse_lessons_from_html(self, html, with_data=True):
        host = self.host
        protocol = self.protocol
        lessons = {}
        soup = BeautifulSoup(html, "html.parser")

        ul = soup.find('ul', class_='lesson-list')
        if ul is None:
            return lessons

        for li in ul.children:
            if type(li) == NavigableString:
                continue
            if 'user-state-not_reached' in li.attrs['class']:
                continue

            div = li.find('div', class_=['link', 'title'])

            div.span.decompose()
            if with_data:
                result = self._extract_from_lesson_data(protocol + host + div.attrs['href'])
                if result[0]:
                    lessons[div.decode_contents().strip()] = [result[1], 'lesson']
            else:
                lessons[div.decode_contents().strip()] = [protocol + host + div.attrs['href'], 'lesson']
        return lessons

    def _extract_from_lesson_data(self, url) -> dict:
        phpsessid5 = self.phpsessid5
        headers = self.headers

        response = requests.get(url, cookies={'PHPSESSID5': phpsessid5}, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        err_div = soup.find('div', style='border: 3px dashed red; padding: 30px; padding-top: 10px; margin-top: 20px; ')
        if err_div and err_div.find('h3') and err_div.find('h3').text == 'Нет доступа':
            return {'success': False, 'message': 'Нет доступа к уроку'}

        if soup.find('span', class_='lesson-description-value') is None:
            description = ''
        else:
            description = soup.find('span', class_='lesson-description-value').text

        audios = []
        files = []
        images = []
        text = ''.encode('utf-8')
        blocks = soup.find('div', class_='lite-page block-set').find_all()
        for div in blocks:
            it_block = div.find('div', class_='lt-block')
            if not it_block:
                continue

            if 'lt-modal-block' in it_block.attrs['class']:
                continue

            if 'lt-lesson-audio' in it_block.attrs['class']:
                scripts = it_block.find_all('script')
                for script in scripts:
                    if 'jPlayerPlaylist' in script.text:
                        text_script = script.decode_contents().strip()
                        start = 0
                        stop = 0
                        i = 0
                        while i < len(text_script):
                            if start == 0 and text_script[i:i + 6] == 'mp3: "':
                                start = i + 6
                                i += 6
                                continue
                            if start != 0 and text_script[i] == '"':
                                stop = i
                                break
                            i += 1
                        url = text_script[start:stop]
                        audios.append(url)
                continue

            if it_block.find_all('button'):
                continue

            if 'lt-lesson-files' in it_block.attrs['class']:
                a = it_block.find('a')
                files.append({'filename': a.get_text(strip=True), 'url': a.attrs['href']})
                continue
            for img in it_block.find_all('img'):
                images.append('https:' + img.attrs['src'])
            for p in it_block.find_all('p'):
                text += p.text.encode('utf-8') + '\n'.encode('utf-8')

        videos = []
        for div in soup.find_all('div', id='player'):
            videos.append({'url': div.attrs['data-plyr-embed-id'], 'type': 'youtube'})
        for iframe in soup.find_all('iframe', class_='vhi-iframe js--vhi-iframe'):
            url = iframe.attrs['src']
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup.find_all('script'):
                if 'window.configs' in script.text:
                    data = script.decode_contents().strip()
                    data = json.loads(data.replace('window.configs = ', ''))
                    m3u8 = data['masterPlaylistUrl']
                    videos.append({'url': m3u8, 'type': 'm3u8'})
                    break

        for audio in soup.find_all('audio'):
            audios.append(audio.attrs['src'])

        return {'success': True, 'data': {'description': description, 'text': text, 'videos': videos, 'audios': audios,
                                          'images': images, 'files': files}}
