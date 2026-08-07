from pathlib import Path
import json

PROJECT_NAME = "MRGpt"

# -----------------------------
# Directories
# -----------------------------
directories = [

    "assets",
    "assets/fonts",
    "assets/icons",
    "assets/images",
    "assets/themes",
    "assets/translations",

    "config",

    "core",
    "core/browser",
    "core/network",
    "core/profile",
    "core/database",
    "core/download",
    "core/security",
    "core/utils",

    "models",

    "services",

    "ui",
    "ui/windows",
    "ui/widgets",
    "ui/dialogs",
    "ui/sidebar",
    "ui/toolbar",
    "ui/statusbar",

    "connections",

    "profiles",

    "downloads",

    "cache",

    "logs",

    "temp",

    "plugins",

    "tests"
]

# -----------------------------
# Python Files
# -----------------------------

python_files = [

    "main.py",

    "core/__init__.py",

    "core/browser/__init__.py",
    "core/browser/browser.py",
    "core/browser/browser_page.py",
    "core/browser/browser_view.py",
    "core/browser/tab_manager.py",

    "core/network/__init__.py",
    "core/network/connection_manager.py",
    "core/network/proxy_manager.py",

    "core/profile/__init__.py",
    "core/profile/profile_manager.py",

    "core/database/__init__.py",
    "core/database/database.py",

    "core/download/__init__.py",
    "core/download/download_manager.py",

    "core/security/__init__.py",
    "core/security/incognito.py",

    "core/utils/__init__.py",
    "core/utils/constants.py",

    "models/__init__.py",

    "services/__init__.py",

    "ui/__init__.py",

    "ui/windows/main_window.py",

    "ui/widgets/address_bar.py",
    "ui/widgets/browser_tab.py",

    "ui/sidebar/sidebar.py",

    "ui/toolbar/toolbar.py",

    "ui/statusbar/statusbar.py",
]

# -----------------------------
# Json Files
# -----------------------------

json_files = {

    "config/settings.json": {

        "language": "fa",

        "theme": "dark",

        "default_font": "Vazirmatn",

        "download_directory": "downloads",

        "private_mode": True,

        "auto_restore_session": False,

        "home_page": "https://www.google.com",

        "connection_profile": None

    },

    "config/browser.json": {

        "zoom": 100,

        "javascript": True,

        "plugins": True,

        "images": True

    },

    "config/network.json": {

        "auto_detect_profiles": True,

        "auto_connect": False,

        "active_profile": ""

    }

}

# -----------------------------
# Create
# -----------------------------

root = Path(PROJECT_NAME)

root.mkdir(exist_ok=True)

for d in directories:
    (root / d).mkdir(parents=True, exist_ok=True)

for f in python_files:

    path = root / f

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("", encoding="utf-8")

for file_name, content in json_files.items():

    path = root / file_name

    path.write_text(
        json.dumps(content, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

print()

print("=" * 60)
print("MRGpt Bootstrap Finished Successfully")
print("=" * 60)

print()

print(root.resolve())