import os
import shutil
import platform
from pathlib import Path
from winregistry import WinRegistry
import vdf
import ctypes  # for Windows popup

# Determine Steam install path
if platform.architecture()[0] == "64bit":
    steam_registry_path = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam"
else:
    steam_registry_path = r"HKEY_LOCAL_MACHINE\SOFTWARE\Valve\Steam"

# Read Steam install path from registry
with WinRegistry() as client:
    steam_path_entry = client.read_entry(steam_registry_path, "InstallPath")
    steam_path = steam_path_entry.value

# Read Steam libraryfolders.vdf
library_vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
if not os.path.exists(library_vdf_path):
    ctypes.windll.user32.MessageBoxW(
        0, f"libraryfolders.vdf not found at {library_vdf_path}", "CS2 Config Copier - Error", 0x10 | 0x1
    )
    exit(1)

with open(library_vdf_path, encoding="utf-8") as f:
    kv = vdf.load(f)

# Find all library folders
library_folders = []
for key, value in kv.get("libraryfolders", {}).items():
    # New Steam format: numbers as keys, paths in strings
    if key.isdigit():
        if isinstance(value, dict) and "path" in value:
            library_folders.append(value["path"])
        elif isinstance(value, str):
            library_folders.append(value)

# Find CS2 (CS:GO) game folder in any library
cs2_game_folder = None
for lib in library_folders:
    cs2_path_candidate = os.path.join(lib, "steamapps", "common", "Counter-Strike Global Offensive", "game", "csgo")
    if os.path.exists(cs2_path_candidate):
        cs2_game_folder = cs2_path_candidate
        break

if cs2_game_folder is None:
    ctypes.windll.user32.MessageBoxW(
        0, "CS2 (CS:GO) game folder not found in any Steam library!", "CS2 Config Copier - Error", 0x10 | 0x1
    )
    exit(1)

# Find all userdata folders (Steam accounts)
userdata_folder = os.path.join(steam_path, "userdata")
user_folders = [f for f in os.listdir(userdata_folder) if os.path.isdir(os.path.join(userdata_folder, f))]

# Files to copy
cfg_files = [
    "autoexec.cfg",
    "cs2_1v1.cfg",
    "cs2_fun.cfg",
    "cs2_nades.cfg"
]

vcfg_files = [
    "cs2_user_convars_0_slot0.vcfg",
    "cs2_user_keys_0_slot0.vcfg",
    "cs2_video.txt",
    "cs2_machine_convars.vcfg"
]

# Source folder (current directory)
src_folder = str(Path().absolute())

# Copy cfg files to game folder
cfg_dst_folder = os.path.join(cs2_game_folder, "cfg")
os.makedirs(cfg_dst_folder, exist_ok=True)
for file_name in cfg_files:
    src_file = os.path.join(src_folder, file_name)
    dst_file = os.path.join(cfg_dst_folder, file_name)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dst_file)
        print(f"Copied {file_name} to {cfg_dst_folder}")

# Copy vcfg files to each user's local cfg folder
for user in user_folders:
    local_cfg_path = os.path.join(userdata_folder, user, "730", "local", "cfg")
    os.makedirs(local_cfg_path, exist_ok=True)
    for file_name in vcfg_files:
        src_file = os.path.join(src_folder, file_name)
        dst_file = os.path.join(local_cfg_path, file_name)
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"Copied {file_name} to {local_cfg_path}")

# Show Windows popup when done
ctypes.windll.user32.MessageBoxW(
    0, "All files have been copied successfully!", "CS2 Config Copier", 0x40 | 0x1
)