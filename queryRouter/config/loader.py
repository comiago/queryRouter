import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, filename: str = "config.yaml"):
        # Risale alla root del progetto
        self.config_path = Path(__file__).parent.parent.parent / filename

    def load(self):
        if not self.config_path.exists():
            return {"default_engine": "https://google.com/search?q=", "shortcuts": {}}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)