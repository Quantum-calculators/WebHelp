from . import cookies as c
from bs4 import BeautifulSoup
import requests


COOKIES_LIST = [
    c.COOKIES1,
    c.COOKIES2,
    c.COOKIES3,
    c.COOKIES4,
    c.COOKIES5,
    c.COOKIES6,
    c.COOKIES7,
    c.COOKIES8,
    c.COOKIES9,
]

class Parser():
    @staticmethod
    def _get_response(url) -> str:
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        i = 0
        status_code = 0
        while i != 7:
            session = requests.session()
            session.headers.update(headers)
            session.cookies.update(COOKIES_LIST[i])
            rs = session.get(url, timeout=3)
            status_code = rs.status_code
            if status_code == 200:
                break
            i += 1
            session.close()
        print(url, "\t", rs.status_code)
        return rs

    @staticmethod
    def _splitting_text_into_words(obj) -> list:
        original_text = obj.get_text()
        text_without_chr10 = original_text.replace(chr(10), ";")
        formatted_text = ""
        buffer = ""

        # Часто при выводе слов попадались следующие ситуации: "ПервоеСлово ВтороеСлово"
        # Цикл ниже проходит по всему тексту и проверяет его на такие ситуации
        i = 0
        while len(text_without_chr10) - 1 != i:
            if (not text_without_chr10[i].isupper()) and text_without_chr10[
                i + 1
            ].isupper():
                buffer += text_without_chr10[i] + " "
            else:
                buffer += text_without_chr10[i]
            i += 1
        i = 0

        # Цикл удаляет повторяющиеся символы точки с запятой
        last_chr = ""
        while len(buffer) - 1 != i:
            if buffer[i + 1] == ";":
                last_chr = ";"
                if buffer[i] != " ":
                    formatted_text += buffer[i]
            else:
                last_chr = ""
            if last_chr != ";":
                formatted_text += buffer[i]
            i += 1

        formatted_text = formatted_text.lower()
        formatted_text = formatted_text.split(";")
        word_list = []
        for i in formatted_text:
            if i:
                word_list.append(i)
        return word_list.copy()

    @staticmethod
    def _get_words_list(html : str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        try:
            body = soup.body
            body_words = Parser._splitting_text_into_words(body)
            
        except:
            body_words = []
            print("The site data was not received")
        return body_words

    def parse(url : str) -> list:
        try:
            items = Parser._get_response(url)
            if items.status_code != 200:
                print([url, [], items.status_code])
                return [url, [], items.status_code]
        except Exception as e:
            print([url, [], 1])
            return [url, [], 1]
        words = Parser._get_words_list(items.text)
        print([url, words, 0])
        return [url, words, 0]


if __name__ == '__main__':
    print(Parser.parse('https://tophotels.ru/'))
    