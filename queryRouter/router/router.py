from ..config import ConfigLoader
from ..models import ParsedQuery

class Router:
    def __init__(self):
        self.loader = ConfigLoader()

    def get_destination(self, parsed: ParsedQuery) -> str:
        data = self.loader.load()
        shortcuts = data.get("shortcuts", {})
        default = data.get("default_engine", "https://www.google.com/search?q=")

        if parsed.keyword in shortcuts:
            conf = shortcuts[parsed.keyword]
            # If the user typed "gm:1" and we have a 'search' template
            if parsed.payload and isinstance(conf, dict) and "search" in conf:
                return conf["search"].replace("{query}", parsed.payload)
            # If they only typed "gm" or there is no search template
            if isinstance(conf, dict):
                return conf.get("url", default + parsed.raw_query)
        
        return f"{default}{parsed.raw_query}"