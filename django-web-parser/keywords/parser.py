from collections import Counter, OrderedDict

import requests
from bs4 import BeautifulSoup
from nltk import RegexpTokenizer, re

from .exceptions import NoKeywordsException, BadURLException


class HTMLParser:
    """
    Abstract class for parsing HTML.
    """

    def __init__(self, url):
        self._url = url

        self._prepare_data()

    def get_result(self, ignore_script):
        raise NotImplementedError

    def _prepare_data(self):
        """Initialize Soup for parsing. """

        try:
            response = requests.get(self._url, timeout=5)

        except requests.RequestException as e:
            raise BadURLException

        self.soup = BeautifulSoup(response.text, "html.parser")


class HTMLKeywordsParser(HTMLParser):
    """
    HTML Parser taking meta keywords and counting occurrences in HTML text.
    """

    def get_result(self, ignore_script):
        """
        Get result of HTML parsing.
        :param ignore_script: Whether taking care of <script> tag.
        :return: {
            'keywords': List of meta keywords,
            'occurrences': SortedDict by keyword occurrences number
        }
        """

        page_meta = self.soup.find_all('meta')

        for meta in page_meta:
            if meta.attrs.get('name', '').lower() == 'keywords':
                keywords_content = meta.attrs['content']

                if not keywords_content:
                    raise NoKeywordsException

                break
        else:
            raise NoKeywordsException

        keywords = self._extract_keywords(keywords_content)
        re_keywords = '|'.join(keywords)

        # ignore all <script> data
        if ignore_script:
            for item in self.soup(['script']):
                item.extract()

        html_keyword_occurrences = self._get_html_occurrences(re_keywords)
        counts = Counter(html_keyword_occurrences)

        # ensure that keyword not exising in text gets as result 0
        ignored_case_counts = {
            keyword: counts.get(keyword.lower(), 0)
            for keyword in keywords
        }

        return {
            'keywords': keywords,
            'occurrences': OrderedDict(sorted(ignored_case_counts.items(), key=lambda x: x[1], reverse=True))
        }

    def _extract_keywords(self, keyword_html_content):
        """Method to extract keywords from HTML meta tag"""

        # remove any special chars like \n
        cleaned_html = ' '.join(keyword_html_content.split())

        # split by dot followed by space to avoid splitting web addresses
        dot_separated = cleaned_html.split('. ')

        # split by comma
        comma_separated = [item.strip().split(',') for item in dot_separated]

        keywords = [item.strip() for sublist in comma_separated for item in sublist ]

        return keywords

    def _get_html_occurrences(self, pattern):
        """Method for getting list of all occurrences in HTML of a given `pattern`"""

        tokenizer = RegexpTokenizer(r'\b(?:%s)\b' % pattern, flags=re.IGNORECASE)

        # input text separated by '\n' for readability
        web_text_parts = "\n".join(self.soup.stripped_strings)

        # get all occurrences in text
        web_tokens = tokenizer.tokenize(web_text_parts)

        # convert to lower names
        web_tokens_lower_names = map(str.lower, web_tokens)

        return web_tokens_lower_names
