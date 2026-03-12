from ..models import ParsedQuery

class QueryParser:
    def __init__(self, separator: str = ":"):
        self.separator = separator

    def parse(self, raw_text: str) -> ParsedQuery:
        clean = raw_text.strip()
        if self.separator in clean:
            key, val = clean.split(self.separator, 1)
            return ParsedQuery(keyword=key.strip().lower(), payload=val.strip(), raw_query=raw_text)
        return ParsedQuery(keyword=clean.lower(), payload=None, raw_query=raw_text)