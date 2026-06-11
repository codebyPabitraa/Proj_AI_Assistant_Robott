from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

SETTINGS_FILE = BASE_DIR / "config" / "settings.yaml"

MODEL_FILE = BASE_DIR / "config" / "model_config.yaml"


class ConfigLoader:

    def __init__(self):

        self.settings = self.load_yaml(SETTINGS_FILE)

        self.models = self.load_yaml(MODEL_FILE)

    @staticmethod
    def load_yaml(path: Path):

        with open(path, "r", encoding="utf-8") as file:

            return yaml.safe_load(file)

    def get_settings(self):

        return self.settings

    def get_models(self):

        return self.models


config = ConfigLoader()