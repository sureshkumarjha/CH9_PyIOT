from icrawler.builtin import BingImageCrawler
from six.moves.urllib.parse import urlparse
from icrawler import ImageDownloader
import base64

urls  = []
class MyImageDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        z = task['file_url']
        url_path = urlparse(task['file_url'])[2]
        urls.append(z)

        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # works for python3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)

def crawl_it(name_to_search):
    google_crawler = BingImageCrawler(
    feeder_threads=1,
    parser_threads=2,
    downloader_threads=4,
    downloader_cls=MyImageDownloader,
    storage={'root_dir': 'images/google'})
    google_crawler.crawl(keyword=name_to_search,  max_num=5, file_idx_offset=0)
    