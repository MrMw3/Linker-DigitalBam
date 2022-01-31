import requests
import re
from urllib.parse import quote
from PyQt5.QtWidgets import QMessageBox

class DigitalBam:
    def __init__(self, instance):
        self.search_page = None
        self.instance = instance

    def get_link(self, user_download_link):
        try:
            if user_download_link.__contains__('/'):
                user_download_link = quote(user_download_link, safe='')
            home_page = requests.get('https://www.digitalbam.ir/Home')
            if home_page.status_code == 200:
                second_url = 'https://www.digitalbam.ir/Home/DetectSearchPrase'
                second_data = {'Phrase': user_download_link}
                self.search_page = requests.post(second_url, data=second_data,
                                                 headers=Headers.second_page(user_download_link))
                if self.search_page.text == 'downloadLink':
                    download_page_url = 'https://www.digitalbam.ir/DirectLinkDownloader/Download'
                    download_page_data = {'downloadUri': user_download_link}
                    download_page = requests.post(download_page_url, data=download_page_data,
                                                  headers=Headers.second_page(user_download_link))
                    if download_page.text.__contains__('fileUrl'):
                        download_link = re.findall('"fileUrl":"(.*)",', download_page.text)
                        # TODO continue this
                        return download_link[0]
                    else:
                        raise Exception('fileUrl not found in response. response: {0}'.format(download_page.text))
                elif self.search_page.text == 'productsSearch':
                    raise Exception('Entered Url is Incorrect')
                else:
                    raise Exception("search page text is contain {0} instead of \"downloadLink\""
                                    .format(self.search_page.text))
            else:
                raise Exception
        except Exception as exc:
            QMessageBox.warning(self.instance, "Error", str(exc))


class Headers:
    def __init__(self):
        pass

    @staticmethod
    def second_page(content):
        data = {
            "Host": "www.digitalbam.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Length": str(len(content)),
            "Origin": "https://www.digitalbam.ir",
            "Connection": "keep-alive",
            "Referer": "https://www.digitalbam.ir/Home",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        return data
