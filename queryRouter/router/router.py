from ..config import ConfigLoader
from ..models import ParsedQuery

class Router:
    def __init__(self):
        self.loader = ConfigLoader()

    def get_destination(self, parsed: ParsedQuery) -> str:
        data = self.loader.load()
        shortcuts = data.get("shortcuts", {})
        default = data.get("default_engine", "https://www.google.com/search?q=")

        target_conf = None
        
        # NEW LOGIC: Loop through keys and support comma-separated aliases
        for key, conf in shortcuts.items():
            # Split "qr, home, dash" into a list: ['qr', 'home', 'dash']
            aliases = [k.strip().lower() for k in key.split(",")]
            
            if parsed.keyword.lower() in aliases:
                target_conf = conf
                break

        # If we found a match, process the URL
        if target_conf:
            if parsed.payload and isinstance(target_conf, dict) and "search" in target_conf:
                return target_conf["search"].replace("{query}", parsed.payload)
            if isinstance(target_conf, dict):
                return target_conf.get("url", f"{default}{parsed.raw_query}")
        
        # Fallback to Google (or your default engine)
        return f"{default}{parsed.raw_query}"