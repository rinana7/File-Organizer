import time
from pathlib import Path
import shutil
from datetime import datetime


TARGET_FOLDER = Path.home()/"Downloads"
LARGE_FILE_THRESHOLD = 500*1024*1024

CATEGORIES = {
    "Images":[".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".dmg", ".pkg", ".sh"],
    "Code Files": [".html", ".py"]
}

def organize_directory():
    if not TARGET_FOLDER.exists():
        return
    for item in TARGET_FOLDER.iterdir():
        if item.is_dir():
            continue
        file_ext = item.suffix.lower()
        file_size = item.stat().st_size
        moved = False

        if file_size > LARGE_FILE_THRESHOLD:
            large_folder = TARGET_FOLDER / "Large Files"
            large_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(large_folder/item.name))
            print(f"Moved Large File: {item.name} -> Large_Files/")
            continue
        mod_time = datetime.fromtimestamp(item.stat().st_mtime)
        year_str = mod_time.strftime("%Y")
        month_str = mod_time.strftime("%m")

        moved = False

        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                category_folder = TARGET_FOLDER/category/year_str/month_str
                category_folder.mkdir(parents=True, exist_ok=True)

                shutil.move(str(item), str(category_folder / item.name))
                print(f"Moved: {item.name} -> {category}/{year_str}/{month_str}/")
                moved = True
                break

        if not moved and file_ext != "":
            others_folder = TARGET_FOLDER/ "Others"/ year_str / month_str
            others_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(others_folder / item.name))
            print(f"Moved: {item.name} -> Others/{year_str}/{month_str}/")


if __name__ == "__main__":
    print("Organizer service running... Press Ctrl+C to stop")
    try:
        while True:
            organize_directory()
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nOrganizer stopped")