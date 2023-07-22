from urllib.request import urlopen
import yt_dlp
from courses_webinars.settings import BASE_DIR
import os


class LoggerOutputs:
    def error(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def debug(self, msg):
        pass
        #print("Captured Log: " + msg)


def save_youtube_video(domen: str, id: str, url: str):
    ydl_opts = {
        "outtmpl": f'{str(BASE_DIR)}/storage/static/{domen}/{id}.%(ext)s',
        "logger": LoggerOutputs()
    }
    filename = ''
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        except yt_dlp.utils.DownloadError as e:
            if 'Video unavailable' in e:
                print('Video unavailable')
            else:
                print(e)
    return '/' + '/'.join(filename.split('\\')[-3:])


def save_m3u8_video(domen: str, id: str, url: str):
    path_to_file = f'{str(BASE_DIR)}\\storage\\static\\{domen}\\{id}.mp4'
    convert_line = f'ffmpeg -hide_banner -loglevel error -protocol_whitelist file,http,https,tcp,tls,crypto -i "{url}" -bsf:a aac_adtstoasc -crf 18 {path_to_file}'
    os.system(convert_line)

    return f'/static/{domen}/{id}.mp4'


def save_file(domen: str, id: str, url: str):
    name = str(id) + '.' + url.split('.')[-1].split('/')[0]
    path_to_save = f'{str(BASE_DIR)}\\storage\\static\\{domen}\\{name}'

    with urlopen(url) as file:
        content = file.read()
    with open(path_to_save, 'wb') as download:
        download.write(content)

    return f'/static/{domen}/{name}'
