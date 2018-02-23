from collections import Counter, OrderedDict

import requests
from bs4 import BeautifulSoup
from nltk import RegexpTokenizer, re


class HTMLParser:

    def __init__(self, url):
        self._url = url

        self._prepare_data()

    def get_result(self):
        raise NotImplementedError

    def _prepare_data(self):

        response = requests.get(self._url)
        self.soup = BeautifulSoup(response.text, "html.parser")


class HTMLKeywordsParser(HTMLParser):

    def get_result(self):
        page_meta = self.soup.find_all('meta')

        keywords = []
        for meta in page_meta:
            if meta.attrs.get('name') == 'keywords':
                keywords = meta.attrs['content'].split(', ')

        # ignore 'style' and 'script'
        for item in self.soup(["script", "style"]):
            item.extract()

        import nltk
        nltk.download('punkt')

        re_keywords = '|'.join(keywords)

        pattern = re.compile(r'\b(?:%s)\b' % re_keywords)
        tokenizer = RegexpTokenizer(pattern)

        text_parts = "\n".join(self.soup.stripped_strings)

        tokens = tokenizer.tokenize(text_parts)

        keyword_tokens = [token for token in tokens if token in keywords]

        counts = Counter(keyword_tokens)

        return OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

