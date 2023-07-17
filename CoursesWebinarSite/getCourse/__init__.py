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

        body = {
            'action': 'processXdget',
            'xdgetId': '99945',  # TODO: Извелкать из первоначальной страницы
            'params[action]': 'login',
            'params[email]': email,
            'params[password]': password
        }

        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Content-Length'] = str(len(body))

        response = requests.post(request_url, data=body, headers=headers)
        result = json.loads(response.text)

        if 'errorMessage' in result:
            return False, result['errorMessage']
        self.phpsessid5 = response.cookies['PHPSESSID5']
        return True, ''

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
            div = li.find('div', class_=['link', 'title'])
            div.span.decompose()
            if with_data:
                data = self._extract_from_lesson_data(protocol + host + div.attrs['href'])
                lessons[div.decode_contents().strip()] = [data, 'lesson']
            else:
                lessons[div.decode_contents().strip()] = [protocol + host + div.attrs['href'], 'lesson']
        return lessons

    def _extract_from_lesson_data(self, url):
        host = self.host
        protocol = self.protocol
        phpsessid5 = self.phpsessid5
        headers = self.headers

        response = requests.get(url, cookies={'PHPSESSID5': phpsessid5}, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find('h2', class_='lesson-title-value').text
        description = soup.find('span', class_='lesson-description-value').text

        text = ''
        div = soup.find('div', class_='f-text')
        if not (div is None):
            text = div.text

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

        urls_audios = []
        for audio in soup.find_all('audio'):
            urls_audios.append(audio.attrs['src'])

        images = []
        for img in soup.find_all('div', class_='image-wrapper'):
            images.append(protocol + img.find('img').attrs['src'])

        return {'title': title, 'description': description, 'text': text, 'videos': videos, 'audio': urls_audios,
                'images': images}