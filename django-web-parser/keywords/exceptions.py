
class NoKeywordsException(Exception):
    """Website does not contains any keywords in <meta> tag"""
    pass


class BadURLException(Exception):
    """Website does not exists in a given URL"""
    pass
