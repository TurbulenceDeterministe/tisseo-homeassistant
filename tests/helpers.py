"""Load the API client without importing Home Assistant's integration entrypoint."""
import importlib
import sys
from pathlib import Path
from types import ModuleType

PACKAGE = "tisseo_under_test"
package = ModuleType(PACKAGE)
package.__path__ = [str(Path(__file__).resolve().parents[1] / "custom_components/tisseo")]
sys.modules[PACKAGE] = package
api = importlib.import_module(f"{PACKAGE}.api_client")
