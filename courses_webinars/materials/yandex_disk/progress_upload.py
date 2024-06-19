import math
import os


class ProgressUpload:
    def __init__(self, callback, filename, chunk_size=1250):
        self.filename = filename
        self.callback = callback
        self.chunk_size = chunk_size
        self.file_size = os.path.getsize(filename)
        self.size_read = 0
        self.divisor = min(math.floor(math.log(self.file_size, 1000)) * 3, 9)  # cap unit at a GB
        self.unit = {0: 'B', 3: 'KB', 6: 'MB', 9: 'GB'}[self.divisor]
        self.divisor = 10 ** self.divisor

    def __iter__(self):
        with open(self.filename, 'rb') as f:
            for chunk in iter(lambda: f.read(self.chunk_size), b''):
                self.size_read += len(chunk)
                yield chunk
                percentage = self.size_read / self.file_size * 100
                self.callback(percentage)

    def __len__(self):
        return self.file_size
