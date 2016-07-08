import os
import importlib

settings_path = os.environ.get("SETTINGS_MODULE")
if settings_path:
    settings_module = importlib.import_module(settings_path)
else:
    try:
        settings_module = importlib.import_module("settings.local")
    except ImportError:
        settings_module = importlib.import_module("settings.common")

globals().update({
    key: value
    for key, value in settings_module.__dict__.items()
    if not key.startswith("__")
})

