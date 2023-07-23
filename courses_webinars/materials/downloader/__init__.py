from urllib.request import urlopen
import yt_dlp
import os
import uuid
from ffmpeg_progress_yield import FfmpegProgress


class Downloader:
    def __init__(self, base_dir):
        self._base_dir = str(base_dir)

    def save_youtube_video(self, url: str):
        base_dir = self._base_dir

        self._check_path()

        ydl_opts = {
            "outtmpl": f'{base_dir}/temp/%(title)s.%(ext)s'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            print(filename)
            return True, filename
        except yt_dlp.utils.DownloadError as e:
            return False, e

    def save_m3u8_video(self, celery_task, url: str):
        base_dir = self._base_dir

        self._check_path()

        try:
            filename = str(uuid.uuid4()) + '.mp4'
            path_to_file = f'{base_dir}/temp/{filename}'

            cmd = [
                "ffmpeg", "-protocol_whitelist", "file,http,https,tcp,tls,crypto", "-i",
                f"{url}", '-bsf:a', 'aac_adtstoasc', "-crf", "18", f"{path_to_file}",
            ]

            ff = FfmpegProgress(cmd)
            for progress in ff.run_command_with_progress():
                celery_task.update_state(state='PROGRESS', meta={'process_percent': progress / 5})
            return True, filename
        except Exception as e:
            return False, e

    def save_file(self, url: str):
        base_dir = self._base_dir

        self._check_path()

        filename = str(uuid.uuid4()) + '.' + url.split('.')[-1].split('/')[0].split('?')[0]
        path_to_save = f'{base_dir}/temp/{filename}'

        try:
            with urlopen(url) as file:
                content = file.read()
            with open(path_to_save, 'wb') as download:
                download.write(content)
            print(filename)
            return True, filename
        except Exception as e:
            return False, e

    def remove(self, filename: str):
        base_dir = self._base_dir

        try:
            path_to_file = f'{base_dir}/temp/{filename}'
            os.remove(path_to_file)
            print(filename)
            return True, ''
        except Exception as e:
            return False, e

    def _check_path(self):
        base_dir = self._base_dir
        if not os.path.exists(f'{base_dir}/temp/'):
            os.mkdir(f'{base_dir}/temp/')
