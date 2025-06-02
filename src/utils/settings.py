import json
from pathlib import Path
from typing import Any, Dict

class Settings:
    _instance = None
    _settings: Dict[str, Any] = {}
    _default_settings = {
        "settings": {
            "search_engine": "https://duckduckgo.com",
            "home_page": "https://duckduckgo.com",
            "enable_javascript": True,
            "enable_cookies": True,
            "download_path": str(Path.home() / "Downloads"),
            "font_size": 14,
            "enable_bookmarks_bar": True,
            "enable_status_bar": True,
            "proxy": {
                "enabled": False,
                "server": ""
            }
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._settings_file = Path(__file__).parent.parent / 'user' / 'settings.json'
        self._load()

    def _load(self):
        try:
            if self._settings_file.exists():
                self._settings = json.loads(self._settings_file.read_text(encoding='utf-8'))
                # make sure all default settings exist, add any missing ones
                self._merge_defaults(self._settings["settings"], self._default_settings["settings"])
            else:
                self._settings = self._default_settings.copy()
                self._save()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self._settings = self._default_settings.copy()

    def _merge_defaults(self, current: Dict[str, Any], defaults: Dict[str, Any]):
        # merge the defaults recursively into the current settings
        for key, value in defaults.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                self._merge_defaults(current[key], value)

    def _save(self):
        try:
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)
            self._settings_file.write_text(
                json.dumps(self._settings, indent=4, sort_keys=True),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, *keys: str, default: Any = None) -> Any:
        current = self._settings
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def set(self, *keys: str, value: Any):
        if not keys:
            return

        current = self._settings
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        self._save()

    def reset(self, *keys: str):
        if not keys:
            self._settings = self._default_settings.copy()
            self._save()
            return

        try:
            current_default = self._default_settings
            for key in keys:
                current_default = current_default[key]

            current = self._settings
            for key in keys[:-1]:
                current = current[key]
            current[keys[-1]] = current_default
            self._save()
        except KeyError:
            pass

settings = Settings()