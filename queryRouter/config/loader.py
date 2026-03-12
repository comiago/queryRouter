import yaml
import os
import logging
from pathlib import Path

# Create a logger specific to the config loader
logger = logging.getLogger("queryRouter.loader")

class ConfigLoader:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._cache = None
            cls._instance._last_mtime = 0
        return cls._instance

    def __init__(self, filename: str = "config.yaml"):
        if not hasattr(self, 'config_path'):
            self.config_path = Path(__file__).parent.parent.parent / filename

    def load(self):
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}. Using defaults.")
            return {"default_engine": "https://www.google.com/search?q=", "shortcuts": {}}
        
        current_mtime = os.path.getmtime(self.config_path)
        
        if self._cache is None or current_mtime > self._last_mtime:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    # 'or {}' prevents errors if the file is completely empty
                    self._cache = yaml.safe_load(f) or {} 
                self._last_mtime = current_mtime
                logger.info("🔄 YAML configuration loaded/reloaded into memory.")
            except yaml.YAMLError as e:
                logger.error(f"❌ Failed to parse YAML file: {e}")
                # Return the old cache if parsing fails, so the app doesn't crash
                return self._cache if self._cache else {"shortcuts": {}}
            
        return self._cache

    def save(self, data: dict):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
            self._cache = data
            self._last_mtime = os.path.getmtime(self.config_path)
            logger.info("💾 YAML configuration successfully saved to disk.")
        except Exception as e:
            logger.error(f"❌ Failed to save YAML file: {e}")