# File Organizer Utility

An automated, background file management utility built in Python for macOS. It periodically scans a specified directory (e.g., `Downloads`), categorizes files by type, organizes them into date-based subdirectories, isolates large files, and maintains an undo history for easy reversal.

---

## Features

- **Automated Scanning:** Runs continuously in the background at set intervals.
- **Category & Extension Mapping:** Automatically routes files into dedicated folders (`Images`, `Documents`, `Audio`, `Videos`, `Archives`, `Executables`, and `Others`).
- **Date-Based Organization:** Structures destination folders by modification year and month (`Category/YYYY/MM/`).
- **Large File Filtering:** Isolates files exceeding 500 MB into a dedicated `Large_Files` directory.
- **Undo Capability:** Tracks move operations in `history.json` to allow reversing the organized files back to their original locations.

---

## Project Structure

```text
File-Organizer/
├── organizer.py        # Main Python script containing sorting and undo logic
├── history.json        # Log file tracking file move operations (generated at runtime)
├── .gitignore          # Excludes build artifacts and history logs from Git
└── README.md           # Project documentation