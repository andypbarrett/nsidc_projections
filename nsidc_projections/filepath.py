"""Sets filepaths for gpd and mapx files"""
import yaml
from pathlib import Path

CONFIG_FILE_PATH = Path("config.yml")


def read_config():
    """Loads config parameters"""
    with open(CONFIG_FILE_PATH) as f:
        return yaml.safe_load(f)


configuration = read_config()

MAPXMAPS_PATH = Path(configuration.get("APP").get("MAPXPATH"))
