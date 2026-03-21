# AutoConfigCopier

Automatically copies your CS2 (Counter-Strike 2 / CS:GO (under maintenance)) configuration files to the correct game and user folders.

## Features

- Copies game `.cfg` files (autoexec, custom configs) to the CS2 game `cfg` folder.
- Copies user-specific `.vcfg` files and `cs2_video.txt` to all Steam users' local cfg folders.
- Automatically detects Steam installation and all library folders.
- Works on any PC, regardless of Steam or CS2 installation paths.
- Shows a Windows popup when copying is complete.

## How to Use

1. Place all your configuration files in the same folder as the `.exe`.
   - Example files:
     - `autoexec.cfg`
     - `cs2_1v1.cfg`
     - `cs2_fun.cfg`
     - `cs2_nades.cfg`
     - `cs2_user_convars_0_slot0.vcfg`
     - `cs2_user_keys_0_slot0.vcfg`
     - `cs2_video.txt`
     - `cs2_machine_convars.vcfg`
2. Run the `.exe` file.
3. The program will automatically copy the files to the correct CS2 folders.
4. A Windows popup will confirm when all files are successfully copied.

## Requirements

- Windows OS
- Steam installed with CS2/CS:GO
- No installation of Python or libraries required if using the `.exe`.

## Notes

- The program works for multiple Steam accounts on the same PC.
- Make sure the config files are named correctly; otherwise, they won’t be copied.
